import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini

st.set_page_config(
    page_title="AI Health & Fitness Planner",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding: 2rem;
        background-color: #f8fafc;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #4f46e5;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #4338ca;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    .success-box {
        padding: 1.5rem;
        border-radius: 0.75rem;
        background-color: #f0fdf4;
        border: 1px solid #86efac;
        margin: 1rem 0;
    }
    
    .warning-box {
        padding: 1.5rem;
        border-radius: 0.75rem;
        background-color: #fef3c7;
        border: 1px solid #fcd34d;
        margin: 1rem 0;
    }
    
    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        margin: 1rem 0;
    }
    
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1e293b;
    }
    
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    
    .stSelectbox>div>div>div {
        border-radius: 8px;
    }
    
    .stNumberInput>div>div>input {
        border-radius: 8px;
    }
    
    div.stMarkdown p {
        line-height: 1.6;
    }
    
    div[data-testid="stHeader"] {
        background-color: white;
        padding: 2rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        margin-bottom: 2rem;
    }
    
    .info-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        margin: 1rem 0;
    }
    
    .metric-card {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.75rem;
        border: 1px solid #e2e8f0;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def create_metric_card(label, value, icon):
    st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.875rem; color: #64748b;">{icon} {label}</div>
            <div style="font-size: 1.25rem; font-weight: 600; color: #0f172a; margin-top: 0.5rem;">{value}</div>
        </div>
    """, unsafe_allow_html=True)

def display_dietary_plan(plan_content):
    with st.expander("📋 Your Personalized Dietary Plan", expanded=True):
        st.markdown("""<div class="info-card">""", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 Why this plan works")
            st.info(plan_content.get("why_this_plan_works", "Information not available"))
            st.markdown("### 🍽️ Meal Plan")
            st.markdown(f"""<div class="success-box">{plan_content.get("meal_plan", "Plan not available")}</div>""", unsafe_allow_html=True)
        
        with col2:
            st.markdown("### ⚠️ Important Considerations")
            considerations = plan_content.get("important_considerations", "").split('\n')
            for consideration in considerations:
                if consideration.strip():
                    st.warning(consideration)
        st.markdown("""</div>""", unsafe_allow_html=True)

def display_fitness_plan(plan_content):
    with st.expander("💪 Your Personalized Fitness Plan", expanded=True):
        st.markdown("""<div class="info-card">""", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 Goals")
            st.success(plan_content.get("goals", "Goals not specified"))
            st.markdown("### 🏋️‍♂️ Exercise Routine")
            st.markdown(f"""<div class="success-box">{plan_content.get("routine", "Routine not available")}</div>""", unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 💡 Pro Tips")
            tips = plan_content.get("tips", "").split('\n')
            for tip in tips:
                if tip.strip():
                    st.info(tip)
        st.markdown("""</div>""", unsafe_allow_html=True)

def main():
    if 'dietary_plan' not in st.session_state:
        st.session_state.dietary_plan = {}
        st.session_state.fitness_plan = {}
        st.session_state.qa_pairs = []
        st.session_state.plans_generated = False

    st.title("🏋️‍♂️ AI Health & Fitness Planner")
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%); 
                    color: white; 
                    padding: 2rem; 
                    border-radius: 0.75rem; 
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);'>
            <h2 style='margin: 0; font-size: 1.5rem; font-weight: 600;'>Welcome to Your Personal Health Journey</h2>
            <p style='margin-top: 1rem; opacity: 0.9;'>Get personalized dietary and fitness plans tailored to your goals and preferences.
            Our AI-powered system considers your unique profile to create the perfect plan for you.</p>
        </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("""
            <div style='background-color: white; padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);'>
                <h3 style='margin: 0; color: #1e293b;'>🔑 API Configuration</h3>
            </div>
        """, unsafe_allow_html=True)
        
        gemini_api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Enter your Gemini API key to access the service"
        )
        
        if not gemini_api_key:
            st.warning("⚠️ Please enter your Gemini API Key to proceed")
            st.markdown("[Get your API key here](https://aistudio.google.com/apikey)")
            return
        
        st.success("✅ API Key accepted!")

    if gemini_api_key:
        try:
            gemini_model = Gemini(id="gemini-1.5-flash", api_key=gemini_api_key)
        except Exception as e:
            st.error(f"❌ Error initializing Gemini model: {e}")
            return

        st.markdown("""
            <div class="info-card">
                <h3 style='margin: 0; color: #1e293b;'>👤 Your Profile</h3>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            age = st.number_input("Age", min_value=10, max_value=100, step=1, help="Enter your age")
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, step=0.1)
            sex = st.selectbox("Sex", options=["Male", "Female", "Other"])
        
        with col2:
            weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, step=0.1)
            activity_level = st.selectbox(
                "Activity Level",
                options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
                help="Choose your typical activity level"
            )
            dietary_preferences = st.selectbox(
                "Dietary Preferences",
                options=["Vegetarian", "Keto", "Gluten Free", "Low Carb", "Dairy Free"],
                help="Select your dietary preference"
            )
        
        with col3:
            if age and weight and height:
                bmi = weight / ((height/100) ** 2)
                create_metric_card("BMI", f"{bmi:.1f}", "📊")
            
            fitness_goals = st.selectbox(
                "Fitness Goals",
                options=["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training"],
                help="What do you want to achieve?"
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎯 Generate My Personalized Plan", use_container_width=True):
            with st.spinner("Creating your perfect health and fitness routine..."):
                try:
                    dietary_agent = Agent(
                        name="Dietary Expert",
                        role="Provides personalized dietary recommendations",
                        model=gemini_model,
                        instructions=[
                            "Consider the user's input, including dietary restrictions and preferences.",
                            "Suggest a detailed meal plan for the day, including breakfast, lunch, dinner, and snacks.",
                            "Provide a brief explanation of why the plan is suited to the user's goals.",
                            "Focus on clarity, coherence, and quality of the recommendations.",
                        ]
                    )

                    fitness_agent = Agent(
                        name="Fitness Expert",
                        role="Provides personalized fitness recommendations",
                        model=gemini_model,
                        instructions=[
                            "Provide exercises tailored to the user's goals.",
                            "Include warm-up, main workout, and cool-down exercises.",
                            "Explain the benefits of each recommended exercise.",
                            "Ensure the plan is actionable and detailed.",
                        ]
                    )

                    user_profile = f"""
                    Age: {age}
                    Weight: {weight}kg
                    Height: {height}cm
                    Sex: {sex}
                    Activity Level: {activity_level}
                    Dietary Preferences: {dietary_preferences}
                    Fitness Goals: {fitness_goals}
                    """

                    dietary_plan_response = dietary_agent.run(user_profile)
                    dietary_plan = {
                        "why_this_plan_works": "High Protein, Healthy Fats, Moderate Carbohydrates, and Caloric Balance",
                        "meal_plan": dietary_plan_response.content,
                        "important_considerations": """
                        - Hydration: Drink plenty of water throughout the day
                        - Electrolytes: Monitor sodium, potassium, and magnesium levels
                        - Fiber: Ensure adequate intake through vegetables and fruits
                        - Listen to your body: Adjust portion sizes as needed
                        """
                    }

                    fitness_plan_response = fitness_agent.run(user_profile)
                    fitness_plan = {
                        "goals": "Build strength, improve endurance, and maintain overall fitness",
                        "routine": fitness_plan_response.content,
                        "tips": """
                        - Track your progress regularly
                        - Allow proper rest between workouts
                        - Focus on proper form
                        - Stay consistent with your routine
                        """
                    }

                    st.session_state.dietary_plan = dietary_plan
                    st.session_state.fitness_plan = fitness_plan
                    st.session_state.plans_generated = True
                    st.session_state.qa_pairs = []

                    display_dietary_plan(dietary_plan)
                    display_fitness_plan(fitness_plan)

                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")

        if st.session_state.plans_generated:
            st.markdown("""
                <div class="info-card">
                    <h3 style='margin: 0; color: #1e293b;'>❓ Questions about your plan?</h3>
                </div>
            """, unsafe_allow_html=True)
            
            question_input = st.text_input("What would you like to know?", key="question_input")

            if st.button("Get Answer", key="get_answer"):
                if question_input:
                    with st.spinner("Finding the best answer for you..."):
                        dietary_plan = st.session_state.dietary_plan
                        fitness_plan = st.session_state.fitness_plan

                        context = f"Dietary Plan: {dietary_plan.get('meal_plan', '')}\n\nFitness Plan: {fitness_plan.get('routine', '')}"
                        full_context = f"{context}\nUser Question: {question_input}"

                        try:
                            agent = Agent(model=gemini_model, show_tool_calls=True, markdown=True)
                            run_response = agent.run(full_context)

                            if hasattr(run_response, 'content'):
                                answer = run_response.content
                            else:
                                answer = "Sorry, I couldn't generate a response at this time."

                            st.session_state.qa_pairs.append((question_input, answer))
                        except Exception as e:
                            st.error(f"❌ An error occurred while getting the answer: {e}")
         

                        if st.session_state.qa_pairs:
                            st.markdown("""
                                <div class="info-card">
                                    <h3 style='margin: 0; color: #1e293b;'>🗣️ Previous Questions & Answers</h3>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            for question, answer in st.session_state.qa_pairs:
                                with st.expander(f"Q: {question}", expanded=True):
                                    st.markdown("""<div class="info-card">""", unsafe_allow_html=True)
                                    st.markdown(f"**Question:** {question}")
                                    st.markdown("**Answer:**")
                                    st.markdown(answer)
                                    st.markdown("""</div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()