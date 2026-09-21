from agentcore.memory import ConversationMemory


def test_add_and_get_history():
    memory = ConversationMemory()
    memory.add_user_message("hello")
    memory.add_assistant_message("hi there")
    history = memory.get_history()
    assert len(history) == 2
    assert history[0]["role"] == "user"


def test_clear():
    memory = ConversationMemory()
    memory.add_user_message("hello")
    memory.clear()
    assert memory.get_history() == []
