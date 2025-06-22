import { Box, Text, Scrollable, Rows } from "@canva/app-ui-kit"
import * as styles from "styles/components.css";
import { Chatbubble } from "./chat_bubble"
import { useAppContext } from "src/context";

export const Chatbox = () => {
  const { messages } = useAppContext();
  return (
    <div>
      <Box border="standard" borderRadius="standard" padding="1u" className={styles.chatContainer}>
        <Scrollable>
          <Rows spacing="1u">
            {messages.length === 0 && <Text tone="secondary">No messages yet</Text>}
            {messages.map((msg, idx) => <Chatbubble content={msg.content} role={msg.role} key={idx} />)}
          </Rows>
        </Scrollable>
      </Box>
    </div>
  )
}

