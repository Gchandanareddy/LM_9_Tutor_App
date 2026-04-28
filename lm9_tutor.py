import streamlit as st

st.set_page_config(
    page_title="Time Series & ICU Tutor",
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
.chat-wrap {
    max-width: 860px; margin: 0 auto;
    padding: 0 1rem 160px 1rem;
}
.msg-ai {
    display:flex; justify-content:flex-start;
    margin:12px 0; gap:10px; align-items:flex-start;
}
.msg-user {
    display:flex; justify-content:flex-end;
    margin:12px 0; gap:10px; align-items:flex-start;
}
.msg-ai .bubble {
    background:#2a2a2a; color:#ececec; padding:14px 18px;
    border-radius:18px 18px 18px 4px; max-width:92%;
    font-size:0.93rem; line-height:1.88;
    border:1px solid #3a3a3a; white-space:pre-wrap;
}
.msg-user .bubble {
    background:#2f2f2f; color:#ececec; padding:12px 16px;
    border-radius:18px 18px 4px 18px; max-width:80%;
    font-size:0.93rem; line-height:1.6; white-space:pre-wrap;
}
.msg-ai .av {
    width:34px; height:34px; border-radius:50%;
    background:linear-gradient(135deg,#ab68ff,#7c3aed);
    display:flex; align-items:center; justify-content:center;
    font-size:1rem; flex-shrink:0; margin-top:2px;
}
.msg-user .av {
    width:34px; height:34px; border-radius:50%;
    background:#19c37d;
    display:flex; align-items:center; justify-content:center;
    font-size:0.75rem; font-weight:700; color:white;
    flex-shrink:0; margin-top:2px;
}
.box-green  { background:#052e16; border-left:4px solid #4ade80; border-radius:0 8px 8px 0; padding:12px 16px; margin:8px 0; color:#bbf7d0; }
.box-yellow { background:#1c1600; border-left:4px solid #fbbf24; border-radius:0 8px 8px 0; padding:12px 16px; margin:8px 0; color:#fef08a; }
.box-red    { background:#1f0a0a; border-left:4px solid #f87171; border-radius:0 8px 8px 0; padding:12px 16px; margin:8px 0; color:#fca5a5; }
.box-blue   { background:#0f1f2e; border-left:4px solid #38bdf8; border-radius:0 8px 8px 0; padding:12px 16px; margin:8px 0; color:#bae6fd; }
.box-purple { background:#1a1a2e; border-left:4px solid #818cf8; border-radius:0 8px 8px 0; padding:12px 16px; margin:8px 0; color:#c7d2fe; }
.tag-py { background:#34d39922; color:#a7f3d0; border:1px solid #34d399; border-radius:12px; padding:2px 10px; font-size:0.78rem; font-weight:600; margin-right:4px; }
.tag-q  { background:#7c3aed33; color:#c4b5fd; border:1px solid #7c3aed; border-radius:12px; padding:2px 10px; font-size:0.78rem; font-weight:600; margin-right:4px; }
.progress-bar-wrap { position:fixed; top:0; left:0; right:0; height:3px; z-index:9999; background:#333; }
.progress-bar-fill { height:100%; background:linear-gradient(90deg,#7c3aed,#19c37d); transition:width 0.5s; }
.top-bar { position:sticky; top:0; background:#212121; border-bottom:1px solid #333; padding:10px 0 8px; margin-bottom:6px; z-index:100; }
.top-bar h2 { text-align:center; font-size:0.9rem; font-weight:500; color:#aaa; margin:0; }
.stButton > button { background:#2a2a2a!important; color:#ececec!important; border:1px solid #444!important; border-radius:20px!important; font-size:0.82rem!important; padding:5px 14px!important; transition:all 0.15s!important; }
.stButton > button:hover { background:#3a3a3a!important; border-color:#7c3aed!important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# TASK DEFINITIONS
# Rules:
#   - nudges = Socratic questions only, never reveal the answer
#   - code_errors = point at specific bug and ask a guiding question
#   - check_kw = keywords that indicate student understands the concept
# ═══════════════════════════════════════════════════════════════

TASKS = [

  # ── Q1 Part 1: What is a sliding window ─────────────────────
  {
    "id":"q1_sw",
    "qnum":"Q1",
    "title":"Q1 — What is a Sliding Window?",
    "icon":"🪟",
    "intro":"""<strong>Question 1: Sliding Window Classification on Time Series</strong>

<div class='box-purple'>
Time series data is a sequence of values recorded over time — a patient's heart rate every minute, ECG signals 500 times per second, blood glucose every hour.

To classify time series data, we need a way to turn a long raw sequence into fixed-size examples a model can learn from. That is what the <strong>sliding window</strong> does.
</div>

Let's start at the very beginning.""",
    "sub_steps":[
      {
        "ask":"In plain English — no code yet — what is a sliding window and why do we need it to apply a standard classifier to time series data? What problem does it solve?",
        "nudges":[
          "Think about what a standard classifier like logistic regression or a decision tree expects as input. Can it accept a sequence of 10,000 readings directly? What format does it need?",
          "A sliding window extracts a fixed-size 'snapshot' of the sequence at each position. If HR readings are [72, 75, 80, 78, 74, 71, 69 ...] and your window size is 3, the first window is [72,75,80], the second is [75,80,78], and so on. What shape does the resulting dataset have?",
          "The key insight: a sliding window converts one variable-length time series into MANY fixed-size feature vectors. Each window becomes one training example. Why does that make standard ML algorithms applicable?"
        ],
        "check_kw":["fixed","size","window","sequence","vector","convert","example","classifier","slice","extract","feature"],
        "code_errors":{},
      },
      {
        "ask":"Now describe the construction precisely. Given a series of length N, window size W, and step size S — how many windows are produced? What does each window contain? Write Python code to implement this.",
        "nudges":[
          "Number of windows = floor((N - W) / S) + 1. Try N=10, W=3, S=1: floor(7/1)+1 = 8 windows. Trace positions 0,1,2 then 1,2,3 ... that gives 8 windows of width 3. Does that match?",
          "Python: X=[]; for i in range(0, N-W+1, S): X.append(series[i:i+W]); X = np.array(X). The shape of X is (num_windows, W). Each row is one example.",
          "What is the loop bound? If N=10 and W=3, the last valid start position is i=7 (window covers indices 7,8,9). So range goes to N-W+1=8. Why +1?"
        ],
        "check_kw":["N","W","S","floor","range","loop","append","np.array","shape","step","windows","index"],
        "code_errors":{
          "wrong_bound":("N-W+1","The loop should go range(0, N-W+1, S). Without the +1 you miss the last valid window. Without -W you'd create partial windows that go out of bounds."),
          "no_step":("S","Your range needs the step argument: range(0, N-W+1, S). Without S the default step is 1 — is that what you want?"),
          "no_array":("np.array","After the loop convert to numpy: X = np.array(X). What shape does it have?"),
        },
      },
      {
        "ask":"How do you assign a LABEL to each window? There is no single correct way — describe TWO different labeling strategies and explain when each is appropriate.",
        "nudges":[
          "Strategy 1 — LAST POINT label: assign the window the class of its final time step. If the last reading is during a seizure, the window is labeled 'seizure'. When is this most useful for real-time systems?",
          "Strategy 2 — MAJORITY VOTE label: assign the class that appears most often in the window. If 7 of 10 steps are 'normal', label the window 'normal'. What goes wrong if the event is very rare — say only 1 step out of 10 is 'event'?",
          "Strategy 3 — CENTER label: use the class of the middle time step. This reduces edge bias. In what scenario would center labeling accidentally introduce future information into training?"
        ],
        "check_kw":["label","last","majority","center","strategy","class","assign","vote","event","point","window"],
        "code_errors":{},
      },
    ]
  },

  # ── Q1 Part 2: Entire series vs individual windows ───────────
  {
    "id":"q1_diff",
    "qnum":"Q1",
    "title":"Q1 — Entire Series vs. Individual Windows",
    "icon":"📈",
    "intro":"""<div class='box-purple'>
Two different classification settings:

<strong>A) Classify the ENTIRE series</strong>
→ One label per complete recording
→ Example: does this 24-hour ECG recording show atrial fibrillation? (yes/no per patient)

<strong>B) Classify INDIVIDUAL WINDOWS</strong>
→ One label per window, many windows per series
→ Example: is THIS 5-minute window of vital signs showing deterioration? (updated every minute)

These have fundamentally different data structures, class imbalance levels, and evaluation needs.
</div>""",
    "sub_steps":[
      {
        "ask":"Give one concrete medical example for EACH approach. Then explain: what is fundamentally different about the prediction task and how a 'training example' is defined in each case?",
        "nudges":[
          "Entire series example: classify a patient's full night of sleep-study data as 'sleep apnea' or 'normal'. One night = one recording = one label. The model makes ONE decision per recording.",
          "Individual windows: monitor ICU patients every minute. Every 5-minute window gets a new prediction: is this patient about to deteriorate? The model makes MANY decisions per patient per day.",
          "Key difference: entire series = retrospective (you have the full recording, make one diagnosis). Individual windows = prospective/real-time (each window is a new decision as new data arrives). How does this affect what features you can use?"
        ],
        "check_kw":["entire","window","ecg","icu","retrospective","prospective","real-time","label","example","one","many","recording"],
        "code_errors":{},
      },
      {
        "ask":"Describe THREE key differences between the two approaches in terms of: (1) data leakage risk, (2) class imbalance, and (3) evaluation strategy. Be specific.",
        "nudges":[
          "LEAKAGE: If you split WINDOWS randomly into train/test, adjacent windows from the same patient end up in both sets. Why is that a form of leakage? What shared information do adjacent windows contain?",
          "CLASS IMBALANCE: A patient has a cardiac event for 3 minutes during a 6-hour ICU stay. With 1-minute windows that is 3 positive windows out of 360. What is the class ratio? How does that compare to whole-series labeling where the label is simply 'had an event today' (1) vs. 'did not' (0)?",
          "EVALUATION: If your window classifier correctly labels 357 out of 360 windows but misses all 3 event windows — what is accuracy? What is recall? For a monitoring alarm system, which metric matters more and why?"
        ],
        "check_kw":["leakage","patient","split","imbalance","rare","recall","precision","accuracy","evaluation","window","adjacent","monitor","event"],
        "code_errors":{},
      },
      {
        "ask":"How do you correctly split a windowed dataset to avoid leakage?\n<span class='tag-py'>Python</span> Write code that splits by PATIENT — not by window — ensuring no patient appears in both train and test.",
        "nudges":[
          "Wrong approach: train_test_split(X_windows, y_windows) randomly assigns individual windows to train/test. Patient A's window 1 is in train, window 2 is in test. These are almost identical — this is leakage.",
          "Correct approach: get unique patient IDs → split THOSE into train/test → assign all windows of each patient to the correct set. Try: train_ids, test_ids = train_test_split(unique_patient_ids, test_size=0.2)",
          "Filter step: train_mask = np.isin(window_patient_ids, train_ids). Then X_train = X[train_mask]; X_test = X[~train_mask]. The array window_patient_ids tracks which patient each window came from."
        ],
        "check_kw":["patient","isin","mask","unique","split","train_ids","test_ids","leakage","window_patient_ids"],
        "code_errors":{
          "split_windows_directly":("train_test_split(X","Splitting on X_windows directly mixes the same patient's windows across train and test. Split on PATIENT IDs first, then use a mask to filter windows."),
          "no_tracking":("window_patient_ids","You need to track which patient each window belongs to. Build this array during window creation alongside X and y."),
          "no_isin":("isin","Use np.isin(window_patient_ids, train_ids) to create a boolean mask, then index X and y with it."),
        },
      },
    ]
  },

  # ── Q2: Longitudinal data ────────────────────────────────────
  {
    "id":"q2_long",
    "qnum":"Q2",
    "title":"Q2 — What is Longitudinal Data?",
    "icon":"📋",
    "intro":"""<strong>Question 2: What is longitudinal data? Is EHR data longitudinal?</strong>

<div class='box-purple'>
The term 'longitudinal' has a specific meaning in data science and statistics. Not every dataset with a timestamp qualifies. Understanding the distinction matters for how you model it and what inferences you can draw.
</div>""",
    "sub_steps":[
      {
        "ask":"Define longitudinal data. What makes it different from cross-sectional data? Give one real-world example of each to make your definition concrete.",
        "nudges":[
          "Cross-sectional: you measure many different subjects at ONE point in time. A health survey of 50,000 people on a single day gives you one measurement per person. You can compare people to each other but cannot track change.",
          "Longitudinal: you measure the SAME subjects repeatedly across time. Following 1,000 patients and recording their blood pressure every year for 10 years gives you 10 observations per person. You can track how each individual changes.",
          "The defining feature is: same entities, multiple time points. This enables studying within-person change, not just between-person differences. Why does that make longitudinal data more powerful for causal inference?"
        ],
        "check_kw":["same","repeated","over time","subject","cross-sectional","change","individual","multiple","track","entity","snapshot"],
        "code_errors":{},
      },
      {
        "ask":"Is EHR data longitudinal? Make a clear argument with specific examples of what EHR data contains.",
        "nudges":[
          "Think about a single patient's EHR: diagnoses from a visit in 2012, medications prescribed in 2015, lab results from 2018, an ICU admission in 2022. Is this the same entity measured at multiple time points?",
          "Yes — EHR IS longitudinal. Patient records span years or decades. The same patient accumulates diagnoses, procedures, medications, and vitals over time. Each encounter adds a new time-stamped observation.",
          "But EHR longitudinal data has complications that structured longitudinal studies do not: irregular visit intervals (patients come when sick, not on schedule), missing data that is not random, patients switching providers. How do these affect your modeling choices?"
        ],
        "check_kw":["yes","ehr","longitudinal","patient","repeated","visit","diagnosis","medication","lab","time","years","same","encounter"],
        "code_errors":{},
      },
      {
        "ask":"Name THREE specific challenges of modeling longitudinal EHR data that you would NOT face with a cross-sectional dataset. For each challenge, propose how you would handle it.",
        "nudges":[
          "Challenge 1 — IRREGULAR INTERVALS: Patient A has visits at months 1, 6, 24 while patient B has visits at months 2, 3, 4, 5. Standard ML algorithms expect aligned, regular inputs. Options: bin visits into yearly periods, forward-fill to a regular grid, or use sequence models (LSTM) that accept variable-length input.",
          "Challenge 2 — INFORMATIVE MISSINGNESS: A missing lab value in an EHR often means the doctor did not order it — which is itself clinical information. Mean imputation treats all missingness equally. What might be more appropriate?",
          "Challenge 3 — VARIABLE SEQUENCE LENGTH: Some patients have 2 visits, others 200. Fixed-size feature matrices require aggressive aggregation (you lose temporal information). What model architectures handle variable-length sequences natively?"
        ],
        "check_kw":["irregular","missing","variable","length","sequence","impute","align","period","aggregate","lstm","temporal","informative","bin","challenge"],
        "code_errors":{},
      },
    ]
  },

  # ── Q3 Part 1: Define the ICU problem ────────────────────────
  {
    "id":"q3_define",
    "qnum":"Q3",
    "title":"Q3-A — ICU System: Define the Problem & Examples",
    "icon":"🏥",
    "intro":"""<strong>Question 3: Design a real-time ICU patient monitoring system.</strong>

<div class='box-purple'>
Inputs available:
• <strong>Vital signs</strong> — HR, BP, SpO2, respiratory rate, temperature recorded continuously (e.g., every minute)
• <strong>Prior diagnoses</strong> — ICD codes from the patient's EHR before ICU admission (static, recorded once at admission)

You must describe every step: define examples → preprocess → build model → test → deploy → justify precision/recall.
</div>

Let's work through this systematically.""",
    "sub_steps":[
      {
        "ask":"What exactly are you predicting? Define the TARGET VARIABLE precisely: what is y=1, what is y=0, and what is the PREDICTION HORIZON (how far into the future)? Justify your choices.",
        "nudges":[
          "Common ICU targets: patient will deteriorate in next 6 hours, sepsis will onset in next 4 hours, patient will die in ICU, patient will need vasopressors within 2 hours. Which is most clinically actionable?",
          "The horizon matters enormously. 1-hour horizon gives less lead time but higher precision — the near future is more predictable. 24-hour horizon gives more warning but the situation may change. How does this trade-off affect clinical utility?",
          "Define concretely: y=1 if [specific event] occurs within [H hours] after observation time T. y=0 otherwise. What is your event, and what is H? Why must this definition be driven by clinical needs, not just statistical convenience?"
        ],
        "check_kw":["target","predict","y=1","y=0","event","horizon","hours","deterioration","sepsis","mortality","label","define","outcome","specific"],
        "code_errors":{},
      },
      {
        "ask":"How do you construct one training EXAMPLE? Describe what X looks like and what y is for one patient at one point in time. How do you ensure the label comes from the FUTURE and features come from the PAST?",
        "nudges":[
          "Think of observation time T. Features X come from the window [T - lookback, T] — e.g., the last 2 hours of vitals. Label y comes from the window (T, T + horizon] — e.g., the next 6 hours. Why must these windows never overlap?",
          "For vital sign features: extract summary statistics over the lookback window for each vital sign — mean, standard deviation, min, max, and trend (slope). This converts the variable-length sequence into a fixed-size numeric vector.",
          "For prior diagnosis features: binary flags (did this patient have diagnosis X before admission?). These are static — they do not change from example to example for the same patient."
        ],
        "check_kw":["T","lookback","horizon","overlap","future","past","feature","label","mean","std","slope","trend","binary","diagnosis","window","static"],
        "code_errors":{},
      },
    ]
  },

  # ── Q3 Part 2: Preprocessing ─────────────────────────────────
  {
    "id":"q3_pre",
    "qnum":"Q3",
    "title":"Q3-B — ICU System: Preprocessing",
    "icon":"⚙️",
    "intro":"""<div class='box-purple'>
Raw ICU data is notoriously messy:
• Monitor artifacts produce physiologically impossible readings
• Vital signs are recorded at different rates (HR every 1 min, BP every 5 min)
• Gaps appear when monitors are disconnected or nurses are repositioning patients
• Prior diagnoses use different coding standards (ICD-9 vs ICD-10) across time
</div>""",
    "sub_steps":[
      {
        "ask":"List FOUR preprocessing steps for ICU vital sign data. For each step, explain what problem it solves and what goes wrong if you skip it.",
        "nudges":[
          "Step 1 — ARTIFACT REMOVAL: A heart rate reading of 0 or 350 bpm is a sensor artifact. If you keep it and compute the mean of a window, how badly does one outlier distort the statistic? How do you identify physiologically impossible values?",
          "Step 2 — MISSING VALUE HANDLING: The SpO2 monitor was disconnected for 15 minutes. Do you forward-fill the last known value? Linearly interpolate? Or flag the gap as its own feature? What are the clinical risks of each choice?",
          "Step 3 — RESAMPLING TO COMMON FREQUENCY: HR is measured every 1 minute, BP every 5 minutes. To compute features over a joint window you need them on the same time grid. How do you upsample BP to 1-minute resolution without inventing false precision?",
          "Step 4 — NORMALIZATION: HR ranges 40-200 bpm, SpO2 ranges 85-100%, temperature 35-42°C. If you feed raw values to a distance-based or gradient-based model, which feature dominates and why? What does z-score normalization do?"
        ],
        "check_kw":["artifact","outlier","missing","impute","resample","normalize","scale","align","frequency","forward fill","interpolate","standardize","common","grid","z-score"],
        "code_errors":{},
      },
      {
        "ask":"For the prior DIAGNOSIS features — each patient may have 0 to 50+ ICD codes before admission. How do you encode these into a fixed-size feature vector?\n<span class='tag-py'>Python</span> Write code using MultiLabelBinarizer.",
        "nudges":[
          "One approach: one binary column per unique diagnosis code or Elixhauser category. For each patient, 1 if they ever had that diagnosis, 0 if not. The result is a sparse binary matrix.",
          "sklearn has a tool for exactly this: MultiLabelBinarizer. It takes a list of lists (each inner list is one patient's set of codes) and returns a binary matrix. Import it from sklearn.preprocessing.",
          "Code: from sklearn.preprocessing import MultiLabelBinarizer; mlb = MultiLabelBinarizer(); X_diag = mlb.fit_transform(patient_code_lists). What type must patient_code_lists be? What does each row and column represent in X_diag?"
        ],
        "check_kw":["MultiLabelBinarizer","binary","icd","encode","fit_transform","list","matrix","column","flag","diagnosis","patient","sparse"],
        "code_errors":{
          "get_dummies_only":("MultiLabelBinarizer","pd.get_dummies() works on a single categorical column, not a list of codes per patient. For multi-label encoding, use MultiLabelBinarizer from sklearn.preprocessing."),
          "fit_transform_on_test":("mlb.transform","On the TEST set use mlb.transform() only — not fit_transform(). If you refit on test data, the column ordering may change and new codes may appear. Why is that a problem?"),
          "wrong_input":("list of lists","MultiLabelBinarizer expects a list of lists. Each inner list is one patient's set of codes: [['ICD001','ICD005'], ['ICD002'], ['ICD001','ICD007','ICD009'], ...]. Is your input structured this way?"),
        },
      },
    ]
  },

  # ── Q3 Part 3: Model + Testing ───────────────────────────────
  {
    "id":"q3_model",
    "qnum":"Q3",
    "title":"Q3-C — ICU System: Model Construction & Testing",
    "icon":"🤖",
    "intro":"""<div class='box-purple'>
You now have:
• X = vital sign summary features (mean, std, min, max, trend per vital) + binary prior diagnosis flags
• y = 1 if patient deteriorates in next 6 hours, else 0

Challenges:
• <strong>Class imbalance</strong> — most ICU windows are stable (y=0)
• <strong>Temporal leakage</strong> — windows from the same patient must not span train and test
• <strong>Clinical interpretability</strong> — clinicians must understand WHY the alarm fired
</div>""",
    "sub_steps":[
      {
        "ask":"Propose THREE model types for this ICU task. For each: give ONE advantage and ONE limitation SPECIFIC to the real-time ICU monitoring context.",
        "nudges":[
          "Model 1 — LOGISTIC REGRESSION: A clinician can examine the coefficients and understand which vital signs drove the score. That transparency matters in a safety-critical setting. What is the core technical limitation for capturing complex interactions between vitals?",
          "Model 2 — GRADIENT BOOSTED TREES (XGBoost / LightGBM): Handles non-linear interactions between features and mixed feature types (continuous vitals + binary diagnoses) naturally. What challenge does this create for deploying in a real-time system with millisecond latency requirements?",
          "Model 3 — LSTM / RNN: Can consume the raw sequence of vital signs without manual feature extraction, learning temporal patterns automatically. What are the two biggest problems with using a deep learning model in a safety-critical clinical deployment?"
        ],
        "check_kw":["logistic","gradient","boost","lstm","rnn","neural","interpret","non-linear","sequence","latency","deploy","clinical","advantage","limitation","xgboost","transparent"],
        "code_errors":{},
      },
      {
        "ask":"Describe your TESTING STRATEGY. How do you split the data? Which metrics do you report? Write Python code to compute the full evaluation suite.",
        "nudges":[
          "Split rule: by PATIENT and by TIME. All windows for patient A go entirely to train or entirely to test. Test patients should come from a LATER time period. Why do you need both constraints — patient-level AND temporal?",
          "Metric rule: with 95% class-0 examples, a model that always predicts 0 gets 95% accuracy but catches zero events. Which metrics reveal this failure? Hint: think about what happens to precision and recall for a majority-class-only predictor.",
          "Python: from sklearn.metrics import classification_report, roc_auc_score, average_precision_score, confusion_matrix. Print all of them. Why is average_precision_score (AUPRC) sometimes more informative than AUC-ROC for heavily imbalanced data?"
        ],
        "check_kw":["patient","time","split","recall","precision","f1","auc","confusion","imbalance","accuracy","metric","roc","classification_report","temporal"],
        "code_errors":{
          "random_split":("patient","Splitting windows randomly mixes the same patient across train and test. Split by patient ID using GroupKFold or a manual patient-based split."),
          "accuracy_only":("recall","Accuracy is misleading here. A model predicting all zeros achieves 95% accuracy but recall=0. Add recall, precision, F1, AUC, and confusion matrix."),
          "no_threshold_discussion":("threshold","The default 0.5 threshold is rarely optimal for imbalanced clinical data. Show how you would select the operating threshold from the precision-recall curve."),
        },
      },
    ]
  },

  # ── Q3 Part 4: Deploy + P/R ──────────────────────────────────
  {
    "id":"q3_deploy",
    "qnum":"Q3",
    "title":"Q3-D — Deployment, Precision & Recall",
    "icon":"🚀",
    "intro":"""<div class='box-purple'>
Deploying the ICU model means:
• Running a new prediction every minute for every ICU patient
• Triggering nurse alarms when risk score exceeds a threshold
• Operating continuously with no downtime
• Maintaining performance as patient populations shift over time
</div>""",
    "sub_steps":[
      {
        "ask":"Describe the real-time INFERENCE PIPELINE step by step. Starting from a new vital sign reading arriving from a bedside monitor — what happens at each stage until a decision is made about whether to trigger an alarm?",
        "nudges":[
          "Step 1: New reading (e.g., SpO2=88% at 03:47) arrives. It is appended to a rolling per-patient buffer. The oldest reading beyond the lookback window is dropped. What data structure would you use for this buffer?",
          "Step 2: Feature extraction — compute mean, std, min, max, trend of each vital from the rolling buffer. Join with the static diagnosis features loaded at admission. You now have one feature vector X_new.",
          "Step 3: Apply the SAME scaler fitted during training (loaded from disk — never refit at inference time). Step 4: model.predict_proba(X_new)[0,1] gives the risk score. Step 5: if score > threshold → trigger alarm and log the prediction with timestamp and features for audit."
        ],
        "check_kw":["buffer","rolling","feature","predict","threshold","alarm","scaler","pipeline","step","real-time","log","admission","static","new reading"],
        "code_errors":{},
      },
      {
        "ask":"What precision and recall values would be ACCEPTABLE for this ICU monitoring system? Justify your answer by thinking through the clinical consequences of each type of error.",
        "nudges":[
          "FALSE NEGATIVE (missed event, recall failure): The model does NOT fire an alarm but the patient IS deteriorating. What is the clinical consequence? The nurse does not intervene. The patient may progress to septic shock, cardiac arrest, or death. How tolerable is this?",
          "FALSE POSITIVE (false alarm, precision failure): The model fires an alarm but the patient is actually stable. The nurse rushes to the bedside, checks everything, finds nothing wrong. Now multiply this by 8-15 false alarms per shift. What well-documented ICU phenomenon does this cause, and why is it dangerous?",
          "Published ICU early-warning literature typically targets recall ≥ 0.80-0.90 (missing events is unacceptable) and precision ≥ 0.25-0.50 (some false alarms are tolerable). Does that seem right? What hospital-specific factors would shift these targets?"
        ],
        "check_kw":["recall","precision","false positive","false negative","alarm fatigue","consequence","clinical","acceptable","miss","intervention","death","trade-off","nurse","0.8","0.9"],
        "code_errors":{},
      },
      {
        "ask":"What is DISTRIBUTION SHIFT and why is it a serious risk for a deployed ICU model? How would you detect it, and what would you do when you detect it?",
        "nudges":[
          "Distribution shift: the statistical properties of the incoming data change over time relative to what the model was trained on. Example: a new treatment protocol is introduced in your ICU — patients' vital sign patterns under the new protocol differ from those in your training data. Does your model know this?",
          "Detection: monitor the distribution of input features over time. Plot weekly moving averages of each feature. Also monitor the fraction of high-risk predictions — if it suddenly jumps from 15% to 60% of patients, something may have changed in the patient population or the data pipeline.",
          "Response: (1) rolling retraining on the most recent N months of data, (2) trigger a human review when model calibration degrades on a held-out validation cohort, (3) ensemble the original model with a recently retrained one to smooth the transition."
        ],
        "check_kw":["shift","drift","distribution","retrain","monitor","change","detect","feature","output","production","calibration","response","recent","protocol"],
        "code_errors":{},
      },
    ]
  },
]

# ═══════════════════════════════════════════════════════════════
# EVALUATOR
# ═══════════════════════════════════════════════════════════════
def evaluate(task, sub_idx, answer, attempt):
    sub     = task["sub_steps"][sub_idx]
    low     = answer.lower()
    is_code = any(c in answer for c in ["(","import ","def ","df[","np.","pd.","=","for ","sklearn"])

    hits  = sum(1 for kw in sub["check_kw"] if kw.lower() in low)
    total = len(sub["check_kw"])

    errors = []
    if is_code and "code_errors" in sub:
        for key, (pattern, msg) in sub["code_errors"].items():
            if pattern.lower() not in low:
                errors.append(msg)

    if hits >= max(3, int(total * 0.45)) and len(errors) == 0:
        quality = "correct"
    elif hits >= 2 or (is_code and len(errors) <= 1):
        quality = "partial"
    else:
        quality = "rethink"

    nudge_idx = min(attempt, len(sub["nudges"]) - 1)

    if quality == "correct":
        fb = """<div class='box-green'>✅ <strong>Excellent!</strong> You've captured the core ideas clearly and correctly.</div>

Type <strong>next</strong> to continue 👉"""

    elif quality == "partial":
        fb = f"""<div class='box-yellow'>⚠️ <strong>Good thinking — you're on the right track!</strong> Let's sharpen this further.</div>

Think about this 👇
<div class='box-blue'>{sub["nudges"][nudge_idx]}</div>
"""
        if errors:
            fb += "\nAlso check these specific issues in your code:\n"
            for i, e in enumerate(errors[:2]):
                fb += f"\n🔍 <strong>Issue {i+1}:</strong> {e}"
        fb += "\n\nRevise your answer or type <strong>hint</strong> for another nudge."

    else:
        fb = f"""<div class='box-red'>❌ <strong>Not quite yet — let's think through this differently.</strong></div>

Here's a guiding question 👇
<div class='box-blue'>{sub["nudges"][0]}</div>

Take your time, think it through, and try again. Type <strong>hint</strong> for more guidance."""

    return quality, fb


def give_hint(task, sub_idx, hint_count):
    sub = task["sub_steps"][sub_idx]
    idx = min(hint_count, len(sub["nudges"]) - 1)
    return f"""💡 <strong>Hint {idx+1} of {len(sub["nudges"])}:</strong>
<div class='box-blue'>{sub["nudges"][idx]}</div>

Give it another try — I'm pointing the way, not giving the answer 🧭"""


# ═══════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════
def init():
    defs = {
        "messages":[], "task_idx":0, "sub_idx":0,
        "stage":"welcome", "hint_count":0, "attempt":0,
        "grades":{}, "initialized":False, "awaiting_next":False,
    }
    for k, v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v
init()

def ai(t):  st.session_state.messages.append({"role":"ai",   "content":t})
def usr(t): st.session_state.messages.append({"role":"user", "content":t})

# ── Welcome message ──────────────────────────────────────────
WELCOME = """🏥 <strong>Welcome to the Time Series & ICU Monitoring Tutor!</strong>

I'm your AI guide for this assignment on time series classification and real-time ICU monitoring systems.

<div class='box-purple'>
<strong>📋 Three Questions:</strong>

<strong>Q1 — Sliding Window Classification</strong>
&nbsp;&nbsp;• What is a sliding window and how is it constructed?
&nbsp;&nbsp;• How are labels assigned to windows?
&nbsp;&nbsp;• Entire series vs. individual windows: differences in leakage, imbalance, evaluation

<strong>Q2 — Longitudinal Data</strong>
&nbsp;&nbsp;• What is longitudinal data vs. cross-sectional?
&nbsp;&nbsp;• Is EHR data longitudinal?
&nbsp;&nbsp;• Three key challenges of longitudinal EHR modeling

<strong>Q3 — Real-Time ICU Monitoring System</strong>
&nbsp;&nbsp;• Define the prediction target and construct training examples
&nbsp;&nbsp;• Preprocess vital signs and prior diagnoses
&nbsp;&nbsp;• Choose models, test correctly, deploy in real time
&nbsp;&nbsp;• Justify acceptable precision and recall
&nbsp;&nbsp;• Handle distribution shift after deployment
</div>

<strong>How I work:</strong>
🔹 I guide you through each part step by step
🔹 I evaluate your answers and point out specific errors in your reasoning or code
🔹 I NEVER give you the answer — I ask questions until you figure it out
🔹 Type <strong>hint</strong> anytime if you are stuck

Ready? Click <strong>Start</strong> or type anything to begin 👇"""

if not st.session_state.initialized:
    ai(WELCOME)
    st.session_state.initialized = True


def present_current():
    t   = TASKS[st.session_state.task_idx]
    si  = st.session_state.sub_idx
    sub = t["sub_steps"][si]
    if si == 0:
        return (f"{t['icon']} <strong>{t['title']}</strong>  "
                f"<span class='tag-q'>{t['qnum']}</span>\n\n"
                f"{t['intro']}\n\n"
                f"<strong>❓ Let's start:</strong>\n{sub['ask']}")
    else:
        return (f"<strong>❓ Next part — {t['title']}</strong>  "
                f"<span class='tag-q'>{t['qnum']}</span>\n\n"
                f"{sub['ask']}")


NEXT_W = {
    "next","continue","ready","go","yes","ok","sure",
    "move on","proceed","got it","understood","done",
    "next question","start","begin","let's go","lets go"
}

def handle(raw):
    txt = raw.strip()
    if not txt: return
    usr(txt)
    low = txt.lower()

    if "restart" in low:
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    # Welcome → begin
    if st.session_state.stage == "welcome":
        st.session_state.stage = "task"
        ai(f"Let's begin! 🚀\n\n{present_current()}")
        return

    # Done stage
    if st.session_state.stage == "done":
        ai("You've completed the assignment! 🎉 Type <strong>restart</strong> to try again.")
        return

    t  = TASKS[st.session_state.task_idx]
    si = st.session_state.sub_idx

    # Hint request
    if any(w in low for w in ["hint","help","stuck","confused","don't know","idk","no idea","explain","how do i"]):
        hc = st.session_state.hint_count
        ai(give_hint(t, si, hc))
        st.session_state.hint_count = hc + 1
        return

    # Next navigation (only when awaiting)
    if any(w in low for w in NEXT_W) and st.session_state.awaiting_next:
        st.session_state.awaiting_next = False
        st.session_state.hint_count   = 0
        st.session_state.attempt      = 0

        if si + 1 < len(t["sub_steps"]):
            st.session_state.sub_idx = si + 1
            ai(present_current())
        else:
            nxt = st.session_state.task_idx + 1
            st.session_state.sub_idx  = 0
            st.session_state.task_idx = nxt

            if nxt >= len(TASKS):
                st.session_state.stage = "done"
                g = st.session_state.grades
                correct_n = sum(1 for v in g.values() if v == "correct")
                partial_n = sum(1 for v in g.values() if v == "partial")
                score = int(((correct_n + 0.5 * partial_n) / len(TASKS)) * 100)
                icons = {"correct":"✅","partial":"⚠️","rethink":"🔄","":"⬜"}
                rows = "\n".join(
                    f"{icons.get(g.get(t2['id'],''),'⬜')}  {t2['icon']} {t2['title']}"
                    for t2 in TASKS
                )
                ai(f"""🎓 <strong>Assignment Complete! Your Scorecard:</strong>

{rows}

<div class='box-green'>
<strong>Score: {correct_n}/{len(TASKS)} fully correct — {score}%</strong>
{'🌟 Outstanding mastery across all three questions!' if score >= 85 else
 '🎉 Great work! Review the ⚠️ tasks to deepen your understanding.' if score >= 55 else
 '💪 Good effort! Re-read each section and try again.'}
</div>

<strong>Key Takeaways:</strong>

🪟 <strong>Sliding Window</strong>
Converts a raw time series into fixed-size examples. Number of windows = floor((N-W)/S)+1. Label by last point, majority vote, or center. Always split by PATIENT not by window to prevent leakage.

📈 <strong>Series vs. Windows</strong>
Entire series = retrospective diagnosis (one label per recording). Individual windows = real-time monitoring (one label per window, many per patient). Window classification creates extreme class imbalance and high leakage risk if split naively.

📋 <strong>Longitudinal Data</strong>
Same subjects measured repeatedly over time. EHR IS longitudinal — patients accumulate records across years. Challenges: irregular intervals, informative missingness, variable sequence length.

🏥 <strong>ICU Monitoring System</strong>
Define target + horizon → construct examples (features from past, label from future, no overlap) → preprocess vitals (artifact removal, gap handling, resampling, normalization) + diagnoses (MultiLabelBinarizer) → model (LR for interpretability, GBDT for performance, LSTM for sequences) → test by patient+time split with recall/AUC/AUPRC → deploy with rolling buffer → monitor for distribution shift.

⚖️ <strong>Precision / Recall</strong>
Missed events (low recall) = patient deteriorates undetected = dangerous. False alarms (low precision) = alarm fatigue = nurses stop responding = also dangerous. Target recall ≥ 0.80-0.90; precision ≥ 0.25-0.50 is typically acceptable.

Type <strong>restart</strong> to try again! 🔄""")
            else:
                ai(present_current())
        return

    # Evaluate the student's answer
    quality, fb = evaluate(t, si, txt, st.session_state.attempt)
    prev = st.session_state.grades.get(t["id"], "")
    if quality == "correct" or (quality == "partial" and prev != "correct"):
        st.session_state.grades[t["id"]] = quality
    st.session_state.attempt += 1

    total_sub = len(t["sub_steps"])
    if quality == "correct":
        st.session_state.awaiting_next = True
        nav = "the next part" if si + 1 < total_sub else "the next question"
        suffix = f"\n\nType <strong>next</strong> for {nav} 👉"
        ai(fb.replace("Type <strong>next</strong> to continue 👉", "") + suffix)
    else:
        ai(fb)


# ═══════════════════════════════════════════════════════════════
# RENDER
# ═══════════════════════════════════════════════════════════════
tidx  = st.session_state.task_idx
total = len(TASKS)
pct   = (int((tidx / total) * 100) if st.session_state.stage == "task" and tidx < total
         else (100 if st.session_state.stage == "done" else 0))

st.markdown(
    f'<div class="progress-bar-wrap">'
    f'<div class="progress-bar-fill" style="width:{pct}%"></div>'
    f'</div>',
    unsafe_allow_html=True
)

if st.session_state.stage == "task" and tidx < total:
    label = f"{TASKS[tidx]['icon']} {TASKS[tidx]['title']}"
elif st.session_state.stage == "done":
    label = "✅ Complete"
else:
    label = "Ready to begin"

st.markdown(
    f'<div class="top-bar"><h2>🏥 Time Series & ICU Tutor &nbsp;·&nbsp; {label}</h2></div>',
    unsafe_allow_html=True
)

st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "ai":
        st.markdown(
            f'<div class="msg-ai"><div class="av">🎓</div>'
            f'<div class="bubble">{msg["content"]}</div></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="msg-user"><div class="bubble">{msg["content"]}</div>'
            f'<div class="av">You</div></div>',
            unsafe_allow_html=True
        )
st.markdown('</div>', unsafe_allow_html=True)

# Quick buttons
s = st.session_state.stage
cols = st.columns([1, 1, 1, 4])
if s == "welcome":
    with cols[0]:
        if st.button("🚀 Start"):    handle("start");   st.rerun()
elif s == "task":
    with cols[0]:
        if st.button("💡 Hint"):     handle("hint");    st.rerun()
    with cols[1]:
        if st.button("▶️ Next"):     handle("next");    st.rerun()
elif s == "done":
    with cols[0]:
        if st.button("🔄 Restart"):  handle("restart"); st.rerun()

inp = st.chat_input("Type your answer or code… (type 'hint' if stuck)")
if inp:
    handle(inp)
    st.rerun()
