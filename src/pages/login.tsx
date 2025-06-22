import { Text, Title, Rows } from "@canva/app-ui-kit";

export const LoginPage = () => {
  return (
    <Rows spacing="1u">
      <Title alignment="center">Welcome to DAG!</Title>
      <Text>I am your new design agent here to assist with you with all your design needs. I can even edit images for you with just a simple prompt! Just select any image and I can assist.</Text>
      <Text>Please authorize to get started! </Text>
    </Rows>
  )
}
