import { Home } from "src/home";
import { ChatPage, ErrorPage, LoginPage } from "src/pages";

export enum Paths {
  HOME = "/",
  CHAT = "/chat"
}

export const routes = [
  {
    path: Paths.HOME,
    element: <Home />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        element: <LoginPage />,
      },
      {
        path: Paths.CHAT,
        element: <ChatPage />
      }
      // @TODO: Add additional pages and routes as needed.
    ],
  },
];
