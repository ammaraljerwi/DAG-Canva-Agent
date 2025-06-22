import { Box, Text } from "@canva/app-ui-kit"
import type { MessageType } from "src/api"


export const Chatbubble = (message: MessageType) => {

  const isUser = message.role === "user"
  return (
    <Box
      alignItems="end"
      background={isUser ? "neutral" : "page"}
      border="standard"
      borderRadius="standard"
      display="inline-flex"
      flexDirection="row"
      flexWrap="noWrap"
      justifyContent={isUser ? "end" : "start"}
      padding="1u"
    >
      <Text alignment={isUser ? "end" : "start"}
        capitalization="default"
        size="medium"
        variant="regular">
        {message.content}
      </Text>
    </Box>
  )
}
