from crewai.flow import Flow, router, start, listen, or_, human_feedback
from crewai.flow.human_feedback import human_feedback
from story_writer_flow.crews.refiner.refiner import kickoff_refiner_crew
from story_writer_flow.crews.writer.writer import kickoff_writer_crew


class Story_Writer_Flow(Flow):

    @start()
    def get_input(self):
        self.state["topic"] = input("Enter the topic name: ")
        return self.state
    
    @human_feedback(message="approve the message", emit=["go", "exit"], llm="ollama/llama3.1:8b")
    @listen(get_input)
    def human_input(self):
        return f"can the story generation be proceeded on the topic: {self.state["topic"]}"
    
    
    @listen("go")
    def writer_crew(self):
        self.state["story"] = kickoff_writer_crew(
            {"topic": self.state["topic"]}
        ).raw
       

    @listen("exit")
    def ending(self):
        print("The crew has ended")

    @listen(writer_crew)
    def refiner_crew(self):
        self.state["refined_story"] = kickoff_refiner_crew(
            {"story": self.state["story"]}
        ).raw

        print("----------------- STORY ----------------")
        print(self.state["refined_story"])

        return self.state["refined_story"]

    
    

def kickoff():
    flow = Story_Writer_Flow()
    return flow.kickoff()


if __name__ == "__main__":
    kickoff()