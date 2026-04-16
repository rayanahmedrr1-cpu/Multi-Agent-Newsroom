from orchestrator.state_machine import StateMachine
from orchestrator.utils import generate_run_id
from orchestrator.logger import log_event
from schemas.message_schema import create_message

# dummy agents (replace later)
def reporter_agent(input_data):
    return {"headline": "Dummy News", "body": "Some news"}

def fact_checker_agent(input_data):
    return {"score": 80, "verdict": "PASS"}

def editor_agent(input_data):
    return {"decision": "APPROVED"}

def publisher_agent(input_data):
    return {"published": True}


def run_pipeline(topic, seed):
    sm = StateMachine()
    run_id = generate_run_id()

    # REPORTER
    sm.transition("REPORTING")
    reporter_output = reporter_agent({"topic": topic, "seed": seed})
    msg1 = create_message(run_id, "REPORTER", {}, reporter_output, "SUCCESS")
    log_event(msg1)

    # FACT CHECK
    sm.transition("FACT_CHECKING")
    fact_output = fact_checker_agent(reporter_output)
    msg2 = create_message(run_id, "FACT_CHECKER", reporter_output, fact_output, "SUCCESS")
    log_event(msg2)

    # EDITOR
    sm.transition("EDITING")
    editor_output = editor_agent(fact_output)
    msg3 = create_message(run_id, "EDITOR", fact_output, editor_output, "SUCCESS")
    log_event(msg3)

    # FINAL STATE
    if editor_output["decision"] == "REJECTED":
        sm.transition("REJECTED")
    else:
        sm.transition("PUBLISHED")

    publisher_output = publisher_agent(editor_output)
    msg4 = create_message(run_id, "PUBLISHER", editor_output, publisher_output, "SUCCESS")
    log_event(msg4)

    return publisher_output
