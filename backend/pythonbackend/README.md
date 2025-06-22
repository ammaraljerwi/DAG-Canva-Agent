# The Agentic Backend for DAG

Agent workflow:
An orchestrator agent will determine the intent of the user's query and utilize the correct tool for the request.
The design feedback tool uses the connect api to asynchronously retrieve the design and provide feedback and return to the main agent.
The edit image tool gets a selection url from the frontend and processes the request using openAIs image model, returning the result and url of the uploaded image.
