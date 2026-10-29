
# STEP 6: Connect Groq AI to TravelMate Chatbot

import streamlit as st
from groq import Groq

from travel_tools import calculate_budget

# Page configuration
st.set_page_config(
    page_title="TravelMate AI",
    page_icon="✈️",
    layout="centered"
)
def go_to_section(section_name):
    st.session_state["section"] = section_name

# STEP 11 FIX: Initialize AI client and instructions before navigation

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

system_prompt = """
You are TravelMate AI, a friendly travel planning assistant.
Help users plan trips, create itineraries, and estimate travel costs.
Ask follow-up questions when important details are missing.
Clearly label prices as estimates, not verified live prices.
Never claim to have booked flights, hotels, or tickets.
Keep responses clear, organized, and beginner-friendly.
"""


# App heading

# STEP 9: Add Top Navigation Bar

st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: #f4f7fb;
}

.travelmate-brand {
    font-size: 24px;
    font-weight: 700;
    padding-top: 6px;
}

.travelmate-caption {
    color: #aab8cc;
    font-size: 12px;
}

div[role="radiogroup"] {
    gap: 5px;
}

div[role="radiogroup"] label {
    background-color: #1a2230;
    border: 1px solid #29364a;
    border-radius: 10px;
    padding: 7px 10px;
}

div[role="radiogroup"] label:hover {
    border-color: #3984f7;
}
</style>
""", unsafe_allow_html=True)

brand_col, nav_col = st.columns([1.15, 4])

with brand_col:
    st.markdown(
        '<div class="travelmate-brand">✈️ TravelMate AI</div>'
        '<div class="travelmate-caption">Your personal travel planner</div>',
        unsafe_allow_html=True
    )


with nav_col:
    section = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "🗺️ AI Trip Planner",
            "💰 Budget Calculator",
            "💬 Travel Assistant"
        ],
        horizontal=True,
        label_visibility="collapsed",
        key="section"
    )


st.divider()

# STEP 10: Create the Home Dashboard

if section == "🏠 Home":
    st.title("Welcome to TravelMate AI! ✈️")
    st.write(
        "Your smart travel companion for planning trips, "
        "exploring destinations, and managing your budget."
    )

    st.divider()

    st.subheader("What would you like to do today?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🗺️ AI Trip Planner")
        st.write("Plan your trip with a personalized itinerary.")

    if st.button(
    "Plan My Trip",
    use_container_width=True,
    on_click=go_to_section,
    args=("🗺️ AI Trip Planner",)
):pass

    st.markdown("### 💰 Budget Calculator")
    st.write("Estimate your travel expenses.")

    if st.button(
    "Calculate Budget",
    use_container_width=True,
    on_click=go_to_section,
    args=("💰 Budget Calculator",)
):pass

    with col2:

        
        st.markdown("### 💬 Travel Assistant")
        st.write("Chat with AI for travel-related help.")

        
    if st.button(
    "Start Chatting",
    use_container_width=True,
    on_click=go_to_section,
    args=("💬 Travel Assistant",)
):pass

    st.info(
        "TravelMate AI provides estimated travel information. "
        "Please verify prices and bookings independently."
    )

    st.stop()
    
# STEP 11: Create the AI Trip Planner
# Ensure Groq client is available for the Trip Planner
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
if section == "🗺️ AI Trip Planner":
    st.title("🗺️ AI Trip Planner")
    st.write("Tell us about your trip and get a personalized itinerary.")

    with st.form("trip_planner_form"):
        destination = st.text_input(
            "Destination",
            placeholder="e.g., Goa"
        )

        days = st.number_input(
            "Trip duration (days)",
            min_value=1,
            max_value=30,
            value=3
        )

        people = st.number_input(
            "Number of travelers",
            min_value=1,
            max_value=20,
            value=2
        )

        budget = st.number_input(
            "Total budget (₹)",
            min_value=1000,
            value=10000,
            step=1000
        )

        interests = st.multiselect(
            "Your interests",
            [
                "Nature",
                "Beaches",
                "Adventure",
                "History",
                "Food",
                "Shopping",
                "Culture",
                "Relaxation"
            ]
        )

        submitted = st.form_submit_button(
            "✨ Generate My Itinerary",
            use_container_width=True
        )

    if submitted:
        if not destination.strip():
            st.warning("Please enter your destination.")
        else:
            with st.spinner("Creating your travel itinerary..."):
                try:
                    prompt = f"""
                    Create a practical travel itinerary.

                    Destination: {destination}
                    Duration: {days} days
                    Travelers: {people}
                    Total budget: ₹{budget}
                    Interests: {", ".join(interests) if interests else "General sightseeing"}

                    Include:
                    1. A day-by-day itinerary.
                    2. Morning, afternoon, and evening activities.
                    3. Estimated expenses in INR.
                    4. Budget-saving tips.
                    5. A total estimated budget breakdown.

                    Keep the plan realistic and organized.
                    Clearly state that prices are estimates, not live prices.
                    Do not claim to book anything.
                    """

                    plan_response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[
                            {
                                "role": "system",
                                "content": system_prompt
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.7,
                        max_tokens=1800
                    )

                    st.markdown("## Your Personalized Itinerary")
                    st.markdown(
                        plan_response.choices[0].message.content
                    )

                except Exception as error:
                    st.error("Unable to generate the itinerary.")
                    print(f"Trip Planner error: {error}")

    st.stop()
    
# STEP 12: Create the Budget Calculator

if section == "💰 Budget Calculator":
    st.title("💰 Travel Budget Calculator")
    st.write("Enter your estimated expenses to calculate your trip budget.")

    with st.form("budget_calculator_form"):
        days = st.number_input(
            "Trip duration (days)",
            min_value=1,
            max_value=30,
            value=3
        )

        people = st.number_input(
            "Number of travelers",
            min_value=1,
            max_value=20,
            value=2
        )

        daily_food = st.number_input(
            "Daily food cost per person (₹)",
            min_value=0,
            value=500,
            step=100
        )

        daily_travel = st.number_input(
            "Daily local travel cost per person (₹)",
            min_value=0,
            value=300,
            step=100
        )

        hotel_per_night = st.number_input(
            "Hotel cost per night for the group (₹)",
            min_value=0,
            value=1500,
            step=500
        )

        activities_per_person = st.number_input(
            "Daily activities cost per person (₹)",
            min_value=0,
            value=400,
            step=100
        )

        calculate = st.form_submit_button(
            "Calculate Total Budget",
            use_container_width=True
        )

    if calculate:
        result = calculate_budget(
            days=int(days),
            people=int(people),
            daily_food=float(daily_food),
            daily_travel=float(daily_travel),
            hotel_per_night=float(hotel_per_night),
            activities_per_person=float(activities_per_person)
        )

        st.subheader("Your Estimated Trip Budget")
        st.write(result)
        st.caption(
            "These are estimates based on your inputs, not live travel prices."
        )

    st.stop()





# Initialize conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 Welcome to TravelMate AI!\n\n"
                "Tell me your destination, trip duration, "
                "budget, and travel interests. Let's plan your trip!"
            )
        }
    ]

# Create Groq client securely
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# AI instructions
system_prompt = """
You are TravelMate AI, a friendly travel planning assistant.

Your responsibilities:
1. Help users plan trips and itineraries.
2. Ask follow-up questions when important details are missing.
3. Suggest activities based on the destination and user interests.
4. Give approximate budget breakdowns when enough information is available.
5. Clearly state that costs are estimates, not verified live prices.
6. Never claim to have booked flights, hotels, or tickets.
7. Remember the conversation context when answering follow-up questions.
8. Keep responses clear, organized, and beginner-friendly.
9. If a user changes their budget or preferences, revise the plan accordingly.
10. If the user asks for a travel budget estimate, collect:
    - Number of days
    - Number of people
    - Daily food cost per person
    - Daily local travel cost per person
    - Hotel cost per night for the group
    - Daily activity cost per person

11. Do not invent expense values. Ask the user for missing values
    or clearly label any suggested values as estimates.

12. Explain that the budget calculator can calculate the total
    once all required values are available.
"""

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Where would you like to travel?")


# STEP 8: Connect the AI to the Python Budget Calculator

import json

budget_tool = [
    {
        "type": "function",
        "function": {
            "name": "calculate_budget",
            "description": "Calculate the estimated cost of a trip using the supplied expense values.",
            "parameters": {
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "description": "Number of trip days"
                    },
                    "people": {
                        "type": "integer",
                        "description": "Number of travelers"
                    },
                    "daily_food": {
                        "type": "number",
                        "description": "Daily food cost per person in INR"
                    },
                    "daily_travel": {
                        "type": "number",
                        "description": "Daily local travel cost per person in INR"
                    },
                    "hotel_per_night": {
                        "type": "number",
                        "description": "Hotel cost per night for the group in INR"
                    },
                    "activities_per_person": {
                        "type": "number",
                        "description": "Daily activities cost per person in INR"
                    }
                },
                "required": [
                    "days",
                    "people",
                    "daily_food",
                    "daily_travel",
                    "hotel_per_night",
                    "activities_per_person"
                ],
                "additionalProperties": False
            }
        }
    }
]

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("TravelMate is planning..."):
            try:
                conversation = [
                    {"role": "system", "content": system_prompt},
                    *st.session_state.messages
                ]

                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=conversation,
                    tools=budget_tool,
                    tool_choice="auto",
                    temperature=0.7,
                    max_tokens=1000
                )

                assistant_message = response.choices[0].message

                if assistant_message.tool_calls:
                    conversation.append(
                        assistant_message.model_dump(exclude_none=True)
                    )

                    for tool_call in assistant_message.tool_calls:
                        if tool_call.function.name == "calculate_budget":
                            arguments = json.loads(
                                tool_call.function.arguments
                            )

                            result = calculate_budget(**arguments)

                            conversation.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps(result)
                            })

                    final_response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=conversation,
                        tools=budget_tool,
                        tool_choice="none",
                        temperature=0.7,
                        max_tokens=1000
                    )

                    reply = final_response.choices[0].message.content
                else:
                    reply = assistant_message.content

                if not reply:
                    reply = "Sorry, I couldn't generate a response. Please try again."

                st.markdown(reply)

                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )

            except Exception as error:
                st.error(
                    "TravelMate couldn't complete your request."
                )

                with st.expander("View error details"):
                    st.write(
                        "Please check your API key, internet connection, "
                        "or try again in a moment."
                    )

                print(f"TravelMate error: {error}")