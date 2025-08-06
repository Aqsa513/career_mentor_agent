import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from roadmap_tool import get_career_roadmap


load_dotenv()

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
        model="gemini-2.5-flash",
        openai_client=external_client
)
config = RunConfig(
    model=model,
    tracing_disabled=True
)

career_agent = Agent(
    name="Career Mentor Agent",
    instructions="You ask about interest and suggest a career field.",
    model=model
)

skill_agent = Agent(
    name="Skill Agent",
    instructions="You share the roadmap using the get_career_roadmap tool.",
    model=model,
    tools=[get_career_roadmap]
)

job_agent = Agent(
    name="Job Agent",
    instructions="You suggest job titles in the chosen career.",
    model=model
)

# 🔹 Main function
def main():
    print("\n🎓 Career Mentor Agent\n")

    while True:
        interest = input("📝 What are your interests? ➡ ")

        # Get career suggestion
        result1 = Runner.run_sync(career_agent, interest, run_config=config)
        field = result1.final_output.strip()
        print("\n📌 Suggested Career:", field)

        # Get skills roadmap
        result2 = Runner.run_sync(skill_agent, field, run_config=config)
        print("\n📚 Required Skills:", result2.final_output)

        # Get job suggestions
        result3 = Runner.run_sync(job_agent, field, run_config=config)
        print("\n💼 Possible Jobs:", result3.final_output)

        again = input("\n🔁 Do you want to explore another field? (yes/no): ").strip().lower()
        if again not in ('yes', 'y'):
            print("\n🙌 Thanks for using Career Mentor Agent!")
            break

if __name__ == "__main__":
    main()
