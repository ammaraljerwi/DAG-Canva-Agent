import {
  Button,
  MultilineInput,
} from "@canva/app-ui-kit";
import { useAppContext } from "src/context";
import { useIntl } from "react-intl";
import { sendAgentRequest } from "src/api";
import { useSelection } from "utils/use_selection_hook";
import type { ImageRef } from "@canva/asset";
import { getTemporaryUrl, upload } from "@canva/asset";

const pending_message = {
  "role": "agent",
  "content": "Agent is thinking, this may take a while..."
}

export const ChatInput = () => {
  const intl = useIntl();
  const { userId, sessionId, chatInput, setChatInput, messages, setMessages } = useAppContext();
  const selection = useSelection("image");
  const isSelected = selection.count > 0;

  const editImage = async (ref: ImageRef) => {
    const { url } = await getTemporaryUrl({
      type: "image",
      ref
    })

    const agent_query = { user_id: userId, session_id: sessionId, query: chatInput, contains_selection: isSelected, selection_data: url }

    try {
      const agent_response = await sendAgentRequest(agent_query);
      if (agent_response.generated_image) {
        return { url: agent_response.generated_image[0], mimeType: agent_response.image_mimetype, agent_response }
      } else {
        return { url: null, agent_response }
      }
    } catch (e) {
      return { url: null, agent_response: { role: "agent", content: `Error getting response: ${e}` } }
    }

  }

  const process_request_with_selection = async () => {
    let newImage;
    const draft = await selection.read();
    for (const content of draft.contents) {
      newImage = await editImage(content.ref);
      if (newImage.url === null) {
        return { role: "agent", content: newImage.agent_response.message }
      } else {
        const asset = await upload({
          type: "image",
          url: newImage.url,
          mimeType: newImage.mimeType,
          thumbnailUrl: newImage.url,
          parentRef: content.ref,
          aiDisclosure: "app_generated"
        });
        content.ref = asset.ref;
      }
    }
    await draft.save();
    return { role: "agent", content: newImage.agent_response.message }
  }

  const process_request = async () => {
    const agent_query = { user_id: userId, session_id: sessionId, query: chatInput }
    try {
      const agent_response = await sendAgentRequest(agent_query)
      return { role: "agent", content: agent_response.message }
    } catch (e) {
      return { role: "agent", content: `Error getting response: ${e}` }
    }
  }

  const onChatInputChange = (value: string) => {
    setChatInput(value);
  };

  const onSendClick = async () => {
    const usrMsg = { "role": "user", "content": chatInput }
    setMessages(msgs => [...msgs, usrMsg, pending_message])

    if (isSelected && selection.count === 1) {
      const agentMessage = await process_request_with_selection()
      setMessages(msgs => [...msgs.slice(0, msgs.length - 1), agentMessage])
    } else {
      const agentMessage = await process_request();
      setMessages(msgs => [...msgs.slice(0, msgs.length - 1), agentMessage])
    }

    setChatInput("");
  };

  const onEnterPress = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") { onSendClick() }
  }

  const SendButton = () => (
    <Button variant="primary" onClick={onSendClick}>
      {intl.formatMessage({
        defaultMessage: "Send",
        description:
          "A button label to remove all contents of the prompt input field",
      })}
    </Button>
  );
  return (<MultilineInput
    placeholder='type to get started'
    onChange={onChatInputChange}
    onKeyDown={onEnterPress}
    minRows={2}
    footer={
      <SendButton />
    }
    required={true}
  />)
};
