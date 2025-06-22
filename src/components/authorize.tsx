import { requestOpenExternalUrl } from "@canva/platform";
import { getDesignToken } from "@canva/design";
import { auth } from "@canva/user";
import { Paths } from "src/routes";
import { Button, Rows } from "@canva/app-ui-kit";
import { useNavigate } from "react-router-dom";
import { useAppContext } from "src/context";
import { useEffect } from "react";

const authorize_tokens = async () => {
  const userToken = await auth.getCanvaUserToken();
  const designToken = await getDesignToken();

  const response = await fetch(PYTHON_BACKEND + `/api/v1/auth/${designToken.token}`, {
    method: "POST", headers: {
      Authorization: `Bearer ${userToken}`
    }
  })

  const res = await response.json();

  // Yes this is not good, i couldn't get cookies to work properly though
  const userid = res.user_id;
  const designid = res.design_id;

  const db_response = await fetch(PYTHON_BACKEND + "/api/v1/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ "user_id": userid, "design_id": designid })
  })

  return { "user_id": userid, "design_id": designid }
}

export const AuthorizeButton = () => {
  const navigate = useNavigate();
  const { setUserId, setSessionId, setIsAuthorized } = useAppContext();

  useEffect(() => {
    const uuid = crypto.randomUUID();
    setSessionId(uuid);
  }, [])

  const AuthClick = async () => {

    const userinfo = await authorize_tokens();
    setUserId(userinfo.user_id)

    try {
      const params = new URLSearchParams({ "user_id": userinfo.user_id })
      const isAuthorized = await fetch(PYTHON_BACKEND + `/api/v1/auth/is_authorized?${params}`)
      if (!isAuthorized.ok) {
        throw new Error("Could not find token")
      }
      navigate(Paths.CHAT)
    } catch {
      // TODO: add success checks
      const res3 = await fetch(PYTHON_BACKEND + `/api/v1/auth/authorize/${userinfo.user_id}`)
      const data = await res3.json()
      const req = await requestOpenExternalUrl({ url: data.url })
      if (req.status === "completed") {
        navigate(Paths.CHAT)
      }
    }

    setIsAuthorized(true)
  }
  return (
    <Rows spacing="1u">
      <Button variant="primary" onClick={() => AuthClick()}> Authorize </Button>
    </Rows>
  )
}
