import streamlit as st
import json
from agent import run_agent
from jira_writer import push_to_jira
from pathlib import Path
from agent import run_agent, save_to_memory


# 1. PAGE CONFIG MUST BE FIRST
st.set_page_config(
    page_title="Predictive Sprint Forecaster", page_icon="🚀", layout="wide"
)

# --- INJECT CUSTOM CSS FOR JIRA AESTHETICS ---
st.markdown(
    """
    <style>
    /* Force primary buttons to Atlassian Blue */
    div.stButton > button[kind="primary"] {
        background-color: #0052CC;
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: 600;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #0047B3;
    }
    /* Clean up the text area to look more like Jira's editor */
    .stTextArea textarea {
        border-radius: 4px;
        border: 2px solid #DFE1E6;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. Setup Header & Logo
current_dir = Path(__file__).parent
logo_file = current_dir / "logo.png"

col1, col2 = st.columns([1, 8])
with col1:
    # Failsafe if logo doesn't exist, it won't crash the whole app
    if logo_file.exists():
        st.image(str(logo_file), width=80)
with col2:
    st.title("Predictive Sprint Forecaster")

st.markdown("Draft, Review, and Approve Agile plans before pushing to Jira.")
st.divider()

# 3. Setup Session State
if "draft_plan" not in st.session_state:
    st.session_state.draft_plan = None
if "target_project" not in st.session_state:
    st.session_state.target_project = "APP"


# Callback function to add a blank row
def add_subtask(story_index):
    st.session_state.draft_plan["stories"][story_index]["subtasks"].append(
        {"summary": "", "description": ""}
    )


# 4. The Upgraded Intake Form
st.markdown("### Create New Sprint Plan")

# The Complete YinzCam Tricode Directory
YINZCAM_TRICODES = [
    "ABADBC",
    "AHLCLE",
    "AHLLV",
    "CFLCGY",
    "CFLSSK",
    "CFLTOR",
    "CFLWPG",
    "COMMVBR",
    "F1LV",
    "F1PC",
    "F1SS",
    "FABAR",
    "FABHA",
    "FABIR",
    "FABLB",
    "FABRE",
    "FABUR",
    "FACEF",
    "FALEE",
    "FALEI",
    "FASUN",
    "FATOT",
    "FAWOL",
    "IOCCAN",
    "MFFLEAGUE",
    "MFFMNT",
    "MFFNATIONAL",
    "MLSATL",
    "MLSATX",
    "MLSCHI",
    "MLSCIN",
    "MLSCLB",
    "MLSCLT",
    "MLSCOL",
    "MLSDC",
    "MLSHCF",
    "MLSHOU",
    "MLSLA",
    "MLSLAFC",
    "MLSMIN",
    "MLSNSH",
    "MLSNYCFC",
    "MLSPHI",
    "MLSRBNY",
    "MLSRSL",
    "MLSSD",
    "MLSSEA",
    "MLSSKC",
    "MLSSKCTV",
    "MLSTOR",
    "NBADCTN",
    "NBADDEL",
    "NBADSBL",
    "NBADSCW",
    "NBABKN",
    "NBABOS",
    "NBACHA",
    "NBACLE",
    "NBADEN",
    "NBAHOU",
    "NBALAC",
    "NBALAL",
    "NBAMIL",
    "NBAMIN",
    "NBANOP",
    "NBANYK",
    "NBAOKC",
    "NBAOKCTV",
    "NBAORL",
    "NBAPHI",
    "NBAPHX",
    "NBAPOR",
    "NBASAC",
    "NBATOR",
    "NBAUTA",
    "NBAWAS",
    "NCAATXAM",
    "NFLARI",
    "NFLATLFB",
    "NFLATLMBS",
    "NFLBAL",
    "NFLBALTV",
    "NFLBUF",
    "NFLCAR",
    "NFLCHI",
    "NFLCIN",
    "NFLCLE",
    "NFLDAL",
    "NFLDALTV",
    "NFLDEN",
    "NFLDET",
    "NFLGB",
    "NFLGBTV",
    "NFLKC",
    "NFLLAC",
    "NFLLV",
    "NFLMIA",
    "NFLMIN",
    "NFLNO",
    "NFLNYG",
    "NFLNYGTV",
    "NFLNYJ",
    "NFLOAK",
    "NFLPHI",
    "NFLPIT",
    "NFLSEA",
    "NFLSF",
    "NFLTB",
    "NFLTEN",
    "NFLWAS",
    "NHLANA",
    "NHLARI",
    "NHLBOS",
    "NHLBUF",
    "NHLCAR",
    "NHLCBJ",
    "NHLCHI",
    "NHLCOL",
    "NHLDAL",
    "NHLDET",
    "NHLFLA",
    "NHLLAK",
    "NHLMIN",
    "NHLNJD",
    "NHLNJDTV",
    "NHLNSH",
    "NHLNYI",
    "NHLOTT",
    "NHLPIT",
    "NHLSJS",
    "NHLSTL",
    "NHLTBL",
    "NHLTOR",
    "NHLUTA",
    "NHLVGK",
    "NWSLBAY",
    "NWSLHOU",
    "NWSLKC",
    "NWSLLA",
    "NWSLSEA",
    "NWSLUTA",
    "PJLLEAGUE",
    "SFARAN",
    "TENCAO",
    "TENIWTG",
    "TENMIA",
    "TENWS",
    "TENWSO",
    "VENUEAAC",
    "VENUEACR",
    "VENUEAKC",
    "VENUEAMALIE",
    "VENUEANA",
    "VENUEAP",
    "VENUEAUD",
    "VENUEBAA",
    "VENUEBC",
    "VENUEBHA",
    "VENUEBOS",
    "VENUEBPL",
    "VENUEBREEDERS",
    "VENUEBSA",
    "VENUEBUFHMK",
    "VENUEBUFKBC",
    "VENUECAOMON",
    "VENUECAOTOR",
    "VENUECBS",
    "VENUECCA",
    "VENUECFG",
    "VENUECHA",
    "VENUECLBHCS",
    "VENUECMN",
    "VENUECPA",
    "VENUECPKC",
    "VENUECSF",
    "VENUEDAL",
    "VENUEDTC",
    "VENUEEDG",
    "VENUEF1",
    "VENUEFLALA",
    "VENUEFRD",
    "VENUEGB",
    "VENUEGEO",
    "VENUEGIL",
    "VENUEGREYCUP",
    "VENUEICE",
    "VENUEIND",
    "VENUELCA",
    "VENUELVGPP",
    "VENUELVS",
    "VENUEMC",
    "VENUEMIL",
    "VENUEMIN",
    "VENUEMSG",
    "VENUEMSGBCNTHR",
    "VENUEMSGCHITHR",
    "VENUEMSGHLUTHR",
    "VENUEMSGRDOCTY",
    "VENUENA",
    "VENUENFLMIN",
    "VENUENYI",
    "VENUE02",
    "VENUEORLKC",
    "VENUEPAT",
    "VENUEPC",
    "VENUEPHX",
    "VENUEPPG",
    "VENUERGP",
    "VENUERQ",
    "VENUERSL",
    "VENUESAS",
    "VENUESBA",
    "VENUESTLCTR",
    "VENUESTLTHR",
    "VENUETAS",
    "VENUETC",
    "VENUETEN",
    "VENUETMC",
    "VENUETOT",
    "VENUETSA",
    "VENUEUAB",
    "VENUEUBA",
    "VENUEUBZ",
    "VENUEUC",
    "VENUEUEM",
    "VENUEVC",
    "VENUEVSH",
    "VENUEWHA",
    "VENUEWSH",
    "VENUEXEC",
    "WNBACHI",
    "WNBACON",
    "WNBADAL",
    "WNBALVA",
    "WNBAMIN",
    "WNBANYL",
    "WNBAPHO",
    "WNBAWAS",
    "XFLLEAGUE",
    "YCADS",
    "YCAISLINN",
    "YCCONCESSIONS",
    "YCFTP",
    "YCPUBLIC",
    "YCSANDBOX",
    "YCTEST",
    "YCTEST1",
]

# Wrap the form in a bordered container
with st.container(border=True):
    col1, col2 = st.columns(2)

    with col1:
        selected_tricode = st.selectbox(
            "Application Tricode",
            options=YINZCAM_TRICODES,
            index=None,
            placeholder="Search team or tricode...",
            help="Enforces strict naming conventions.",
        )

    with col2:
        project_key = st.selectbox(
            "Jira Project Key",
            options=["APP", "WORK"],
            help="The Jira board where these tickets will live.",
        )

    user_prompt = st.text_area(
        "Feature Description",
        height=150,
        placeholder="e.g., Implement a real-time predictive stats widget for the live game screen...",
    )

    submit_pressed = st.button(
        "⚡ Generate Draft Plan", type="primary", use_container_width=True
    )

# 5. The AI Trigger Logic
if submit_pressed:
    if not selected_tricode:
        st.warning("Please select an Application Tricode to proceed.", icon="⚠️")
    elif not user_prompt:
        st.warning("Please provide a feature description.", icon="⚠️")
    else:
        with st.status("Consulting historical Jira data...", expanded=True) as status:
            st.write("Searching vector database for similar past epics...")
            enriched_prompt = (
                f"App Tricode: {selected_tricode}\n\nFeature Request: {user_prompt}"
            )

            try:
                st.write("Generating structured JSON plan...")
                raw_output = run_agent(enriched_prompt)

                if isinstance(raw_output, str):
                    st.session_state.draft_plan = json.loads(raw_output)
                else:
                    st.session_state.draft_plan = raw_output

                st.session_state.target_project = project_key

                status.update(
                    label="Draft generated successfully!",
                    state="complete",
                    expanded=False,
                )
                st.rerun()
            except Exception as e:
                status.update(label="Generation failed.", state="error")
                st.error(f"Error: {e}")

# 6. The Human-in-the-Loop Approval Form
if st.session_state.draft_plan:
    st.divider()
    st.subheader("2. Human Review & Approval")
    st.info(
        "Review the AI's draft below. Edit details or add new subtasks before creating the tickets."
    )

    plan = st.session_state.draft_plan

    # Epic Details
    st.markdown("### Epic Details")
    epic_summary = st.text_input("Epic Title", value=plan.get("epic_summary", ""))
    epic_description = st.text_area(
        "Epic Description", value=plan.get("epic_description", "")
    )

    st.markdown("### Stories & Subtasks")
    updated_stories = []

    for i, story in enumerate(plan.get("stories", [])):
        with st.expander(f"Story {i+1}: {story.get('summary', 'New')}", expanded=True):
            s_title = st.text_input(
                f"Title", value=story.get("summary", ""), key=f"s_title_{i}"
            )
            s_desc = st.text_area(
                f"Description", value=story.get("description", ""), key=f"s_desc_{i}"
            )

            st.markdown("**Subtasks**")
            updated_subtasks = []

            for j, subtask in enumerate(story.get("subtasks", [])):
                col1, col2 = st.columns([1, 2])
                with col1:
                    sub_sum = st.text_input(
                        f"Subtask {j+1}",
                        value=subtask.get("summary", ""),
                        key=f"sub_sum_{i}_{j}",
                    )
                with col2:
                    sub_desc = st.text_input(
                        f"Details",
                        value=subtask.get("description", ""),
                        key=f"sub_desc_{i}_{j}",
                    )
                updated_subtasks.append({"summary": sub_sum, "description": sub_desc})

            st.button(
                "➕ Add Subtask", key=f"add_sub_{i}", on_click=add_subtask, args=(i,)
            )

            updated_stories.append(
                {
                    "summary": s_title,
                    "description": s_desc,
                    "subtasks": updated_subtasks,
                }
            )

    # Save updates back to session state
    st.session_state.draft_plan["epic_summary"] = epic_summary
    st.session_state.draft_plan["epic_description"] = epic_description
    st.session_state.draft_plan["stories"] = updated_stories

    st.divider()

    # 7. Final Approval, Jira Push, and AI Learning Loop
    if st.button(
        f"✅ Approve Plan & Create in {st.session_state.target_project}",
        type="primary",
        use_container_width=True,
    ):
        with st.spinner(
            f"Pushing live tickets to Jira project {st.session_state.target_project}..."
        ):
            try:
                # 1. Push the tickets to actual Jira
                created_keys = push_to_jira(
                    st.session_state.target_project, st.session_state.draft_plan
                )

                # 2. THE SELF-HEALING TRIGGER: Save the edits back to ChromaDB
                save_to_memory(st.session_state.draft_plan, selected_tricode)

                # 3. Celebrate
                st.success(
                    f"🎉 Success! Created the following tickets: {', '.join(created_keys)} \n\n🧠 AI Memory updated with your human-approved layout!"
                )
                st.balloons()
            except Exception as e:
                st.error(f"Failed to create tickets or save to memory. Error: {e}")
