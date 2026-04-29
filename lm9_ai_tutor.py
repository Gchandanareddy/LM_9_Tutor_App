import streamlit as st
import json
import urllib.request
import urllib.error

st.set_page_config(
    page_title="LM9 — Time Series & ICU Tutor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #212121; color: #ececec; }
header[data-testid="stHeader"] { background: transparent; }
.chat-wrap { max-width: 860px; margin: 0 auto; padding: 0 1rem 160px 1rem; }
.msg-ai   { display:flex; justify-content:flex-start;  margin:12px 0; gap:10px; align-items:flex-start; }
.msg-user { display:flex; justify-content:flex-end;    margin:12px 0; gap:10px; align-items:flex-start; }
.msg-ai .bubble { background:#2a2a2a; color:#ececec; padding:14px 18px; border-radius:18px 18px 18px 4px; max-width:92%; font-size:0.93rem; line-height:1.88; border:1px solid #3a3a3a; white-space:pre-wrap; }
.msg-user .bubble { background:#2f2f2f; color:#ececec; padding:12px 16px; border-radius:18px 18px 4px 18px; max-width:80%; font-size:0.93rem; line-height:1.6; white-space:pre-wrap; }
.msg-ai .av { width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#ab68ff,#7c3aed);display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0;margin-top:2px; }
.msg-user .av { width:34px;height:34px;border-radius:50%;background:#19c37d;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;color:white;flex-shrink:0;margin-top:2px; }
.box-green  { background:#052e16;border-left:4px solid #4ade80;border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0;color:#bbf7d0; }
.box-yellow { background:#1c1600;border-left:4px solid #fbbf24;border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0;color:#fef08a; }
.box-red    { background:#1f0a0a;border-left:4px solid #f87171;border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0;color:#fca5a5; }
.box-blue   { background:#0f1f2e;border-left:4px solid #38bdf8;border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0;color:#bae6fd; }
.box-purple { background:#1a1a2e;border-left:4px solid #818cf8;border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0;color:#c7d2fe; }
.tag-py { background:#34d39922;color:#a7f3d0;border:1px solid #34d399;border-radius:12px;padding:2px 10px;font-size:0.78rem;font-weight:600;margin-right:4px; }
.tag-concept { background:#ec489933;color:#f9a8d4;border:1px solid #ec4899;border-radius:12px;padding:2px 10px;font-size:0.78rem;font-weight:600;margin-right:4px; }
.tag-q { background:#7c3aed33;color:#c4b5fd;border:1px solid #7c3aed;border-radius:12px;padding:2px 10px;font-size:0.78rem;font-weight:600;margin-right:4px; }
.ai-badge { background:#7c3aed33;color:#c4b5fd;border:1px solid #7c3aed;border-radius:8px;padding:1px 7px;font-size:0.7rem;font-weight:600;margin-left:5px; }
.progress-bar-wrap { position:fixed;top:0;left:0;right:0;height:3px;z-index:9999;background:#333; }
.progress-bar-fill { height:100%;background:linear-gradient(90deg,#7c3aed,#19c37d);transition:width 0.5s; }
.top-bar { position:sticky;top:0;background:#212121;border-bottom:1px solid #333;padding:10px 0 8px;margin-bottom:6px;z-index:100; }
.top-bar h2 { text-align:center;font-size:0.9rem;font-weight:500;color:#aaa;margin:0; }
.stButton > button { background:#2a2a2a!important;color:#ececec!important;border:1px solid #444!important;border-radius:20px!important;font-size:0.82rem!important;padding:5px 14px!important;transition:all 0.15s!important; }
.stButton > button:hover { background:#3a3a3a!important;border-color:#7c3aed!important; }
</style>
""", unsafe_allow_html=True)

# ── API key ────────────────────────────────────────────────────
def get_api_key():
    try: return st.secrets["ANTHROPIC_API_KEY"]
    except: return st.session_state.get("api_key","")

with st.sidebar:
    st.markdown("### 🔑 API Key")
    k = st.text_input("Anthropic API Key", value=st.session_state.get("api_key",""), type="password", placeholder="sk-ant-...", label_visibility="collapsed")
    if k: st.session_state["api_key"] = k; st.success("✅ Key saved")
    api_key = get_api_key()
    if api_key: st.markdown("<span style='color:#4ade80;font-size:0.82rem'>🤖 AI grading active</span>", unsafe_allow_html=True)
    else:       st.markdown("<span style='color:#fbbf24;font-size:0.82rem'>⚠️ No key — fallback grading</span>", unsafe_allow_html=True)
    st.markdown("---")
    g = st.session_state.get("grades",{})
    st.markdown(f"**Score:** {sum(1 for v in g.values() if v=='correct')} ✅  {sum(1 for v in g.values() if v=='partial')} ⚠️")
    st.caption("📚 HI 780 — LM9: Time Series & ICU Monitoring")

# ═══════════════════════════════════════════════════════════════
# TASKS  — 4 topics, each with sub-steps
# Each sub-step has: ask, nudges, answer_guidance (for AI grader),
#                    check_kw (fallback), code_errors (fallback)
# ═══════════════════════════════════════════════════════════════

TASKS = [
  {
    "id":"q1_sw", "qnum":"Q1", "title":"Q1 — What is a Sliding Window?", "icon":"🪟",
    "intro":"""<strong>Q1: Sliding Window Classification on Time Series</strong>

<div class='box-purple'>
Time series data is a sequence of values recorded over time — a patient's heart rate every minute, ECG signals 500 times per second, blood glucose every hour.

To apply a standard classifier to time series we need a way to turn that long raw sequence into fixed-size examples. That is what the <strong>sliding window</strong> does.
</div>""",
    "sub_steps":[
      {
        "ask":"In plain English — no code yet — what is a sliding window and why do we need it to apply a standard classifier to time series data? What problem does it solve?",
        "answer_guidance":"A sliding window extracts fixed-size slices from a variable-length sequence. Standard classifiers like logistic regression need a fixed-size feature vector. A time series can be thousands of points and vary between patients. The window slides along the timeline (with a configurable step size) and each position produces one fixed-size training example. This converts one long sequence into many fixed-size vectors that a classifier can accept.",
        "nudges":["Think about what a standard classifier expects as input. Can it accept a sequence of 10,000 readings directly?","A sliding window extracts a fixed-size 'snapshot' at each position. If HR readings are [72,75,80,78,74] and window size=3, windows are [72,75,80], [75,80,78]... What shape does the dataset have?","The key: one variable-length series → MANY fixed-size vectors. Each window = one training example."],
        "check_kw":["fixed","size","window","sequence","vector","convert","example","classifier","slice","extract"],
        "code_errors":{},
      },
      {
        "ask":"Describe the construction precisely. Given a series of length N, window size W, step S — how many windows are produced? Write Python code to implement this.",
        "answer_guidance":"Number of windows = floor((N-W)/S)+1. Python: X=[]; for i in range(0, N-W+1, S): X.append(series[i:i+W]); X=np.array(X). Shape of X is (num_windows, W). The loop must go to N-W+1 to include the last valid window. The step S controls overlap — step=1 gives maximum overlap, step=W gives no overlap.",
        "nudges":["Number of windows = floor((N-W)/S)+1. Try N=10,W=3,S=1: floor(7/1)+1=8 windows.","Python: X=[]; for i in range(0, N-W+1, S): X.append(series[i:i+W]); X=np.array(X). Shape=(num_windows,W).","Loop bound: N-W+1. If N=10,W=3 — last valid start is i=7 (window covers 7,8,9). Why +1?"],
        "check_kw":["N","W","S","floor","range","loop","append","np.array","shape","step","windows"],
        "code_errors":{"wrong_bound":("N-W+1","Loop should be range(0,N-W+1,S). Without +1 you miss the last valid window."),"no_step":("S","range needs step: range(0,N-W+1,S)."),"no_array":("np.array","Convert to numpy after loop: X=np.array(X).")},
      },
      {
        "ask":"How do you assign a LABEL to each window? Describe TWO different labeling strategies and when each is appropriate.",
        "answer_guidance":"Strategy 1 — LAST POINT: label by the class of the final time step in the window. Good for real-time systems where you want to know the state right now. Strategy 2 — MAJORITY VOTE: label by the most common class in the window. Good when events are gradual but problematic for rare events (1 positive out of 10 steps = 0 vote). Strategy 3 — CENTER: label by the middle step, reducing edge bias. Risk: center labeling can accidentally use future information in real-time settings.",
        "nudges":["Last point: assign the class of the final time step. When is this useful for real-time early-warning?","Majority vote: most common class across window steps. What happens for very rare events (1 out of 10)?","Center point: class of the middle step. When would this accidentally introduce future information?"],
        "check_kw":["label","last","majority","center","strategy","class","assign","vote","event","point"],
        "code_errors":{},
      },
    ]
  },
  {
    "id":"q1_diff", "qnum":"Q1", "title":"Q1 — Entire Series vs. Individual Windows", "icon":"📈",
    "intro":"""<div class='box-purple'>
Two different classification settings:
<strong>A) Entire series</strong> → one label per complete recording (e.g., does this 24-hr ECG show atrial fibrillation?)
<strong>B) Individual windows</strong> → one label per window, many per series (e.g., is THIS 5-minute window showing deterioration?)
</div>""",
    "sub_steps":[
      {
        "ask":"Give one concrete medical example for EACH approach. Then explain: what is fundamentally different about the prediction task and how a training example is defined?",
        "answer_guidance":"Entire series: classify a full 24-hour Holter ECG recording as 'atrial fibrillation' or 'normal' — one recording = one label = one training example. Retrospective/diagnostic use. Individual windows: ICU monitoring — every 5-minute window of vitals gets a new prediction, updated every minute. Many examples per patient per day. Prospective/real-time use. Key difference: entire series = one decision per patient after full recording. Windows = continuous stream of decisions as data arrives.",
        "nudges":["Entire series: one recording, one label, one decision. E.g., classify a full night of sleep study as 'sleep apnea' yes/no.","Individual windows: many decisions per patient per day. E.g., ICU alarm: is THIS 5-minute window showing deterioration?","Entire = retrospective (review after recording). Windows = prospective (decide as data arrives). How does this affect what features you can use?"],
        "check_kw":["entire","window","ecg","icu","retrospective","prospective","real-time","label","one","many","recording"],
        "code_errors":{},
      },
      {
        "ask":"Describe THREE key differences between the two approaches: (1) data leakage risk, (2) class imbalance, (3) evaluation strategy.",
        "answer_guidance":"1. LEAKAGE: Random split of windows mixes same-patient windows across train/test — adjacent windows share almost identical data. Must split by patient. Entire series: split by patient straightforwardly. 2. CLASS IMBALANCE: Windows create extreme imbalance — a 3-minute cardiac event in a 6-hour stay = 3 out of 360 windows positive (0.8%). Entire series: patient either had an event or not — less extreme. 3. EVALUATION: Windows — accuracy is useless (99.2% accuracy by always predicting 0). Must use recall, F1, AUC-ROC. Recall matters most for safety-critical monitoring.",
        "nudges":["LEAKAGE: Adjacent windows from same patient in both train and test share almost identical data. Why is that leakage?","CLASS IMBALANCE: 3-minute event in 6-hour stay with 1-min windows = 3/360 positive windows. What is that ratio?","EVALUATION: 357/360 windows correct but 0 events caught — what is accuracy? What is recall?"],
        "check_kw":["leakage","patient","split","imbalance","rare","recall","precision","accuracy","evaluation","adjacent","monitor"],
        "code_errors":{},
      },
      {
        "ask":"How do you prevent leakage when splitting a windowed dataset?\n<span class='tag-py'>Python</span> Write code that splits by PATIENT.",
        "answer_guidance":"Split by patient IDs, not by window. train_ids,test_ids=train_test_split(unique_patient_ids,test_size=0.2,random_state=42). Then: train_mask=np.isin(window_patient_ids,train_ids); X_train=X[train_mask]; X_test=X[~train_mask]; y_train=y[train_mask]; y_test=y[~train_mask]. Must track window_patient_ids alongside X and y during window creation.",
        "nudges":["Wrong: train_test_split(X_windows) randomly mixes same-patient windows. Split on patient IDs first.","Correct: train_ids,test_ids=train_test_split(unique_patient_ids). Then use mask.","train_mask=np.isin(window_patient_ids,train_ids). Need window_patient_ids array tracking each window's patient."],
        "check_kw":["patient","isin","mask","unique","split","train_ids","test_ids","window_patient_ids"],
        "code_errors":{"split_windows_directly":("train_test_split(X","Split on patient IDs, not window arrays."),"no_tracking":("window_patient_ids","Track which patient each window belongs to during creation."),"no_isin":("isin","np.isin(window_patient_ids,train_ids) creates the boolean mask.")},
      },
    ]
  },
  {
    "id":"q2_long", "qnum":"Q2", "title":"Q2 — Longitudinal Data & EHR", "icon":"📋",
    "intro":"""<strong>Q2: What is longitudinal data? Is EHR data longitudinal?</strong>

<div class='box-purple'>Not every dataset with a timestamp is truly longitudinal. The distinction matters for modeling choices and what inferences you can draw.</div>""",
    "sub_steps":[
      {
        "ask":"Define longitudinal data. What makes it different from cross-sectional data? Give one real-world example of each.",
        "answer_guidance":"Cross-sectional: measures many different subjects at ONE point in time. E.g., a health survey of 50,000 people today — one measurement per person. Can compare between people but not track change. Longitudinal: measures the SAME subjects REPEATEDLY over time. E.g., measuring the same 1,000 patients' blood pressure every year for 10 years — 10 observations per person. Can track within-person change, not just between-person differences.",
        "nudges":["Cross-sectional: one snapshot of many subjects at one time. Survey of 50,000 people today.","Longitudinal: same subjects at multiple time points. Follow 1,000 patients for 10 years of blood pressure.","Defining feature: SAME entities, MULTIPLE time points. Enables studying within-person change."],
        "check_kw":["same","repeated","over time","subject","cross-sectional","change","individual","multiple","track","snapshot"],
        "code_errors":{},
      },
      {
        "ask":"Is EHR data longitudinal? Make a clear argument with specific examples. Then name THREE specific challenges of longitudinal EHR data.",
        "answer_guidance":"YES — EHR IS longitudinal. The same patient accumulates diagnoses, medications, lab results, procedures, and vitals across years or decades. Each encounter adds a new time-stamped observation of the same entity. THREE challenges: 1. IRREGULAR INTERVALS — patients visit when sick, not on schedule. Different patients have records at different time points. Handle with: bin into periods, forward-fill, or use LSTM for variable-length sequences. 2. INFORMATIVE MISSINGNESS — a missing lab test often means the doctor didn't order it (itself clinical information). Mean imputation assumes random missingness which is wrong. 3. VARIABLE SEQUENCE LENGTH — some patients have 2 visits, others 200. Fixed feature matrices require aggregation that loses temporal information.",
        "nudges":["EHR: same patient, multiple time points (diagnoses 2012, meds 2015, labs 2018, ICU 2022). Longitudinal? Yes.","Challenge 1: irregular intervals — patients visit when sick. Challenge 2: informative missingness — no lab ordered ≠ normal. Challenge 3: variable sequence length.","Handling: bin into yearly periods, forward-fill, LSTM for variable-length sequences, indicator for missing."],
        "check_kw":["yes","ehr","longitudinal","patient","repeated","visit","diagnosis","irregular","missing","variable","length","challenge"],
        "code_errors":{},
      },
    ]
  },
  {
    "id":"q3_icu", "qnum":"Q3", "title":"Q3 — Real-Time ICU Monitoring System", "icon":"🏥",
    "intro":"""<strong>Q3: Design a real-time ICU patient monitoring system.</strong>

<div class='box-purple'>
Inputs: <strong>vital signs</strong> (HR, BP, SpO2, RR, temp — continuous, every minute) + <strong>prior diagnoses</strong> (ICD codes from EHR before admission — static).

Describe: define examples → preprocess → model → test → deploy → justify precision/recall.
</div>""",
    "sub_steps":[
      {
        "ask":"Define the prediction target. What is y=1, y=0, what is the prediction horizon H? How do you construct one training example (X and y)?",
        "answer_guidance":"Target: y=1 if patient deteriorates (e.g., needs vasopressors, transfers to higher care, dies) within the next H hours (e.g., 6 hours). y=0 otherwise. One training example: at observation time T, X = features extracted from the LOOKBACK window [T-120min, T] (mean/std/min/max/trend of each vital sign) + static binary diagnosis flags from admission. y = label from FUTURE window (T, T+360min]. These windows must NEVER overlap — features must come strictly from the past and label strictly from the future. Horizon choice: shorter (1-2hr) = more precise but less lead time; longer (12-24hr) = more warning but harder to predict.",
        "nudges":["y=1 = patient deteriorates within H hours. What specific event? Vasopressors, code, transfer?","X = features from the PAST (mean/std/trend of vitals over last 2 hours + static diagnosis flags). y = label from the FUTURE window. Why must they never overlap?","Horizon H: 6 hours gives clinical lead time. What features from vital signs in the last 2 hours? Mean, std, min, max, trend (slope)."],
        "check_kw":["target","y=1","y=0","horizon","lookback","overlap","future","past","feature","label","mean","std","trend","binary","diagnosis"],
        "code_errors":{},
      },
      {
        "ask":"Describe FOUR preprocessing steps for ICU vital signs and explain how to encode prior diagnoses. Write Python code for the diagnosis encoding.",
        "answer_guidance":"1. ARTIFACT REMOVAL: physiologically impossible values (HR=0,HR=350) → median filter or clip to valid range. If kept, distorts window statistics. 2. MISSING VALUE HANDLING: forward-fill short gaps (<15min) or linear interpolate; flag long gaps as a feature. Missing is often informative. 3. RESAMPLING to common frequency: HR=1min, BP=5min → upsample BP to 1min grid using forward-fill or interpolation. 4. NORMALIZATION: z-score scale each vital sign — otherwise HR (range ~160) dominates SpO2 (range ~15). For diagnoses: MultiLabelBinarizer — each patient has a list of ICD codes, output is binary matrix. mlb=MultiLabelBinarizer(); X_diag=mlb.fit_transform(patient_codes); use mlb.transform() on test set.",
        "nudges":["4 steps: artifact removal, missing value handling, resampling to common frequency, normalization/scaling.","Diagnoses: one binary column per unique ICD/Elixhauser code. MultiLabelBinarizer handles lists of codes per patient.","from sklearn.preprocessing import MultiLabelBinarizer; mlb=MultiLabelBinarizer(); X=mlb.fit_transform(patient_code_lists). Use .transform() on test set only."],
        "check_kw":["artifact","missing","resample","normalize","scale","forward fill","interpolate","MultiLabelBinarizer","binary","icd","fit_transform"],
        "code_errors":{"no_mlb":("MultiLabelBinarizer","Use MultiLabelBinarizer for multi-label ICD encoding — not get_dummies()."),"fit_transform_test":("transform","On test set use mlb.transform() only — not fit_transform().")},
      },
      {
        "ask":"Propose THREE model types with advantages/limitations for ICU monitoring. Describe your testing strategy and which metrics you use.",
        "answer_guidance":"Models: 1. LOGISTIC REGRESSION — interpretable (clinicians see which vitals drove the score), fast inference. Limitation: linear boundary, can't capture complex vital sign interactions. 2. GRADIENT BOOSTED TREES (XGBoost/LightGBM) — captures non-linear interactions, handles mixed feature types. Limitation: harder to explain to clinicians, larger model size. 3. LSTM/RNN — processes raw vital sign sequences, learns temporal patterns automatically. Limitation: needs much more data, black box, harder to deploy in real-time. Testing: split by PATIENT and by TIME (test patients from later periods). Metrics: F1, AUC-ROC, AUPRC (better for heavy imbalance), recall (most critical — missed events = patient dies). Threshold tuning: choose operating point from precision-recall curve.",
        "nudges":["LR: interpretable but linear. GBDT: non-linear but less interpretable. LSTM: sequence-native but needs lots of data.","Split: by patient AND by time. All windows of patient A go to train or test — never both.","Metrics: NOT accuracy (95% class-0 → always predict 0 = 95% accuracy). Use recall, F1, AUC, AUPRC."],
        "check_kw":["logistic","gradient","boost","lstm","interpret","non-linear","sequence","patient","time","split","recall","f1","auc","threshold"],
        "code_errors":{"random_split":("patient","Split by patient ID not by window."),"accuracy_only":("recall","Accuracy is misleading for imbalanced ICU data. Use recall, F1, AUC.")},
      },
      {
        "ask":"Describe the real-time deployment pipeline step by step. What precision and recall are acceptable? What is distribution shift and how do you handle it?",
        "answer_guidance":"Pipeline: 1. New reading arrives → append to rolling per-patient buffer. 2. Extract features (mean/std/min/max/trend per vital from buffer + static diagnosis flags). 3. Apply the SAME scaler fitted at training time (loaded from disk — never refit). 4. model.predict_proba(X_new)[0,1] → risk score. 5. If score > threshold → trigger alarm + log with timestamp. Precision/Recall: Recall ≥ 0.80-0.90 (missing deterioration = patient may die — unacceptable). Precision ≥ 0.25-0.50 acceptable (some false alarms OK, but alarm fatigue is real danger). Distribution shift: input data statistics change over time (new treatment protocol, COVID, different patient population). Detect: monitor weekly moving averages of feature distributions and model output rate. Respond: rolling retraining on recent data, alert when calibration degrades.",
        "nudges":["Pipeline: buffer → features → scale → predict_proba → threshold → alarm/log.","Recall ≥ 0.85: missed events = patient deteriorates undetected. False alarms = alarm fatigue = nurses ignore alarms. Both are dangerous.","Distribution shift: model trained pre-COVID, new COVID patients have different vital patterns. Monitor feature distributions weekly."],
        "check_kw":["buffer","rolling","scaler","predict_proba","threshold","alarm","log","recall","precision","alarm fatigue","distribution shift","retrain","monitor"],
        "code_errors":{},
      },
    ]
  },
]

# ═══════════════════════════════════════════════════════════════
# AI GRADER
# ═══════════════════════════════════════════════════════════════
def call_claude(task_title, question, answer_guidance, student_answer, hint_used, api_key):
    is_code = any(c in student_answer for c in ["(","import ","def ","np.","pd.","sklearn","=","for "])
    type_note = "Python code question — evaluate logic and structure." if is_code else "Conceptual question — evaluate reasoning in plain English."
    system = f"""You are a health informatics professor grading students. {type_note}
NEVER reveal the correct answer. Say what is right, what is missing, ask ONE Socratic question.
Grade: correct=all key concepts present, partial=some right but incomplete, incorrect=wrong or vague.
Return ONLY JSON: {{"grade":"correct|partial|incorrect","feedback":"2-3 sentences","nudge":"one guiding question"}}"""
    user = f"Task: {task_title}\nQuestion: {question}\nAnswer guidance (do NOT reveal): {answer_guidance}\nStudent: {student_answer}\nHint given: {hint_used}"
    payload = json.dumps({"model":"claude-sonnet-4-20250514","max_tokens":500,"system":system,"messages":[{"role":"user","content":user}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages",data=payload,
          headers={"Content-Type":"application/json","x-api-key":api_key,"anthropic-version":"2023-06-01"},method="POST")
    with urllib.request.urlopen(req,timeout=30) as resp: data=json.loads(resp.read())
    raw=data["content"][0]["text"].strip()
    if "```" in raw:
        for part in raw.split("```"):
            part=part.strip().lstrip("json").strip()
            try: r=json.loads(part); return r["grade"],r["feedback"],r["nudge"]
            except: continue
    r=json.loads(raw); return r["grade"],r["feedback"],r["nudge"]

def smart_fallback(sub, answer):
    low=answer.lower(); wc=len(answer.split())
    is_code=any(c in answer for c in ["(","import ","def ","np.","pd.","=","for ","sklearn"])
    hits=sum(1 for kw in sub["check_kw"] if kw.lower() in low)
    total=len(sub["check_kw"])
    errors=[]
    if is_code:
        for key,(pattern,msg) in sub.get("code_errors",{}).items():
            if pattern.lower() not in low: errors.append(msg)
    if wc<8: return "incorrect","Your answer is too brief — please explain more.","What is the core concept here?"
    if hits>=max(3,int(total*0.45)) and len(errors)==0: return "correct","You've covered the key ideas well.",""
    if hits>=2 or (is_code and len(errors)<=1):
        msg2="Also check your code: "+errors[0] if errors else f"{hits}/{total} key concepts found."
        return "partial",msg2,"What else is important to mention here?"
    return "incorrect",f"Missing core concepts ({hits}/{total} found).","What is the main idea this question is testing?"

def grade(sub, title, question, answer_guidance, student_answer, hint_used):
    api_key=get_api_key()
    if api_key and api_key.startswith("sk-"):
        try: return call_claude(title,question,answer_guidance,student_answer,hint_used,api_key)
        except: pass
    return smart_fallback(sub, student_answer)

def render_fb(gv, fb, nudge, title):
    badge="<span class='ai-badge'>🤖 AI</span>" if (get_api_key() and get_api_key().startswith("sk-")) else "<span class='ai-badge'>⚡ Auto</span>"
    if gv=="correct":
        extra=f"\n\n<div class='box-blue'>💡 {nudge}</div>" if nudge else ""
        return f"<div class='box-green'>✅ {badge} <strong>Great work on {title}!</strong>\n{fb}{extra}</div>\n\nType <strong>next</strong> to continue 👉"
    elif gv=="partial":
        return f"<div class='box-yellow'>⚠️ {badge} <strong>On the right track!</strong>\n{fb}</div>\n\n<div class='box-blue'>💭 <strong>Think about:</strong> {nudge}</div>\n\nRevise or type <strong>hint</strong>."
    return f"<div class='box-red'>❌ {badge} <strong>Not quite yet.</strong>\n{fb}</div>\n\n<div class='box-blue'>💭 <strong>Guiding question:</strong> {nudge}</div>\n\nTry again or type <strong>hint</strong>."

# ═══════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════
def init():
    defs={"messages":[],"task_idx":0,"sub_idx":0,"stage":"welcome","hint_count":0,"hint_used":False,"grades":{},"initialized":False,"awaiting_next":False,"pending_answer":None}
    for k,v in defs.items():
        if k not in st.session_state: st.session_state[k]=v
init()
def ai(t): st.session_state.messages.append({"role":"ai","content":t})
def usr(t): st.session_state.messages.append({"role":"user","content":t})

WELCOME="""🏥 <strong>Welcome to the LM9 AI Tutor!</strong>

I'm your AI guide for <em>Time Series Classification & Real-Time ICU Monitoring</em>.

<div class='box-purple'>
<strong>📋 Three Questions:</strong>
<strong>Q1</strong> — Sliding window: construct it, label it, entire series vs windows, prevent leakage
<strong>Q2</strong> — Longitudinal data: definition, EHR as longitudinal, three key challenges
<strong>Q3</strong> — ICU monitoring system: define examples → preprocess → model → test → deploy → precision/recall
</div>

<div class='box-green'>✨ Add your Anthropic API key in the sidebar for full AI grading.</div>

🔹 Type <strong>hint</strong> anytime · Type <strong>next</strong> after a correct answer
Ready? Click <strong>Start</strong> 👇"""

if not st.session_state.initialized: ai(WELCOME); st.session_state.initialized=True

def present_current():
    t=TASKS[st.session_state.task_idx]; si=st.session_state.sub_idx; sub=t["sub_steps"][si]
    tag="<span class='tag-concept'>💬 Conceptual</span>"
    if any(c in sub["ask"] for c in ["Python","code","Write"]): tag="<span class='tag-py'>🐍 Python</span>"
    if si==0:
        return f"{t['icon']} <strong>{t['title']}</strong>  <span class='tag-q'>{t['qnum']}</span> {tag}\n\n{t['intro']}\n\n<strong>❓ Let's start:</strong>\n{sub['ask']}"
    return f"<strong>❓ Next — {t['title']}</strong>  <span class='tag-q'>{t['qnum']}</span> {tag}\n\n{sub['ask']}"

NEXT_W={"next","continue","ready","go","yes","ok","sure","move on","proceed","got it","understood","done","start","begin"}

def process_next():
    st.session_state.awaiting_next=False; st.session_state.hint_count=0; st.session_state.hint_used=False
    t=TASKS[st.session_state.task_idx]; si=st.session_state.sub_idx
    if si+1<len(t["sub_steps"]):
        st.session_state.sub_idx=si+1; ai(present_current())
    else:
        nxt=st.session_state.task_idx+1; st.session_state.sub_idx=0; st.session_state.task_idx=nxt
        if nxt>=len(TASKS):
            st.session_state.stage="done"; g=st.session_state.grades
            c=sum(1 for v in g.values() if v=="correct"); p=sum(1 for v in g.values() if v=="partial")
            score=int(((c+0.5*p)/len(TASKS))*100)
            icons={"correct":"✅","partial":"⚠️","incorrect":"❌","":"⬜"}
            rows="\n".join(f"{icons.get(g.get(t2['id'],''),'⬜')}  {t2['icon']} {t2['title']}" for t2 in TASKS)
            ai(f"""🎓 <strong>LM9 Complete! Scorecard:</strong>\n\n{rows}\n\n<div class='box-green'><strong>Score: {c}/{len(TASKS)} — {score}%</strong></div>\n\n<strong>Key Takeaways:</strong>\n🪟 Sliding window: floor((N-W)/S)+1 windows · label by last/majority/center · split by PATIENT\n📈 Series vs windows: retrospective vs real-time · windows → extreme imbalance · recall matters\n📋 Longitudinal: same subjects over time · EHR IS longitudinal · irregular/missing/variable-length\n🏥 ICU: define target+horizon → lookback features, future label, no overlap → 4 preprocess steps → LR/GBDT/LSTM → patient+time split → recall≥0.85 · alarm fatigue · monitor drift\n\nType <strong>restart</strong> to try again 🔄""")
        else: ai(present_current())

def handle(raw):
    txt=raw.strip(); if not txt: return
    low=txt.lower()
    if "restart" in low:
        for k in list(st.session_state.keys()): del st.session_state[k]; st.rerun()
    if st.session_state.stage=="welcome":
        usr(txt); st.session_state.stage="task"; ai(f"Let's begin! 🚀\n\n{present_current()}"); return
    if st.session_state.stage=="done":
        usr(txt); ai("Complete! Type <strong>restart</strong> to try again."); return
    t=TASKS[st.session_state.task_idx]; si=st.session_state.sub_idx; sub=t["sub_steps"][si]
    if any(w in low for w in ["hint","help","stuck","confused","idk","don't know","no idea"]):
        usr(txt); st.session_state.hint_used=True; hc=st.session_state.hint_count
        idx=min(hc,len(sub["nudges"])-1)
        ai(f"💡 <strong>Hint {hc+1} for {t['title']}:</strong>\n<div class='box-blue'>{sub['nudges'][idx]}</div>\nGive it another try 🧭"); st.session_state.hint_count=hc+1; return
    if any(w in low for w in NEXT_W) and st.session_state.awaiting_next:
        usr(txt); process_next(); return
    usr(txt); st.session_state.pending_answer=txt; ai("🤖 <em style='color:#7c3aed'>Grading...</em>")

def grade_pending():
    txt=st.session_state.pending_answer; t=TASKS[st.session_state.task_idx]; si=st.session_state.sub_idx; sub=t["sub_steps"][si]
    msgs=st.session_state.messages
    if msgs and "Grading" in msgs[-1]["content"]: msgs.pop()
    gv,fb,nudge=grade(sub,t["title"],sub["ask"],sub["answer_guidance"],txt,st.session_state.hint_used)
    prev=st.session_state.grades.get(t["id"],"")
    if gv=="correct" or (gv=="partial" and prev!="correct"): st.session_state.grades[t["id"]]=gv
    feedback=render_fb(gv,fb,nudge,t["title"])
    if gv=="correct":
        st.session_state.awaiting_next=True
        total_sub=len(t["sub_steps"]); nav="next part" if si+1<total_sub else "next question"
        feedback=feedback.replace("Type <strong>next</strong> to continue 👉",f"Type <strong>next</strong> for {nav} 👉")
    ai(feedback); st.session_state.pending_answer=None

if st.session_state.get("pending_answer"): grade_pending()

# ── RENDER ────────────────────────────────────────────────────
tidx=st.session_state.task_idx; total=len(TASKS)
pct=int((tidx/total)*100) if st.session_state.stage=="task" and tidx<total else (100 if st.session_state.stage=="done" else 0)
st.markdown(f'<div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:{pct}%"></div></div>',unsafe_allow_html=True)
label=(f"{TASKS[tidx]['icon']} {TASKS[tidx]['title']}" if st.session_state.stage=="task" and tidx<total else ("✅ Complete" if st.session_state.stage=="done" else "Ready"))
st.markdown(f'<div class="top-bar"><h2>🏥 LM9 AI Tutor &nbsp;·&nbsp; {label}</h2></div>',unsafe_allow_html=True)
st.markdown('<div class="chat-wrap">',unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"]=="ai": st.markdown(f'<div class="msg-ai"><div class="av">🎓</div><div class="bubble">{msg["content"]}</div></div>',unsafe_allow_html=True)
    else: st.markdown(f'<div class="msg-user"><div class="bubble">{msg["content"]}</div><div class="av">You</div></div>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)
s=st.session_state.stage; cols=st.columns([1,1,1,4])
if s=="welcome":
    with cols[0]:
        if st.button("🚀 Start"): handle("start"); st.rerun()
elif s=="task":
    with cols[0]:
        if st.button("💡 Hint"): handle("hint"); st.rerun()
    with cols[1]:
        if st.button("▶️ Next"): handle("next"); st.rerun()
elif s=="done":
    with cols[0]:
        if st.button("🔄 Restart"): handle("restart"); st.rerun()
inp=st.chat_input("Type your answer… (hint / next)")
if inp: handle(inp); st.rerun()
