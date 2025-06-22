import { openDesign } from "@canva/design";
import { Button, Rows } from "@canva/app-ui-kit";
import * as styles from "styles/components.css";
import { requestExport, getDesignToken } from "@canva/design";
import { getTemporaryUrl, upload } from "@canva/asset";
import { addElementAtPoint } from "@canva/design";
import type { DesignEditing } from "@canva/design";
import { useSelection } from "utils/use_selection_hook";
import { auth } from "@canva/user";
import { requestOpenExternalUrl } from "@canva/platform";
import { useAppContext } from "src/context";

// export const TestPage = () => {
//   function handleClick() {
//     openDesign({ type: "current_page" }, async (draft) => {
//       draft.page.elements.forEach((element, index) => {
//         console.log(index, element)
//       });
//     });
//   }
//
//   return (
//     <div className={styles.scrollContainer}>
//       <Rows spacing="2u">
//         <Button variant="primary" onClick={handleClick}>
//           Read design
//         </Button>
//       </Rows>
//     </div >
//   )
// }
//
// export const TestPage = () => {
//   async function handleClick() {
//     const elementsFound = [];
//     openDesign({ type: "current_page" }, async (draft, { elementBuilder }) => {
//       if (draft.page.type !== "fixed") {
//         return;
//       }
//
//       const newRect = elementBuilder.createRectElement({
//         top: 300,
//         left: 300,
//         width: 150,
//         height: 100,
//         fill: {
//           color: {
//             type: "solid",
//             color: "#ff0000",
//           },
//         },
//       });
//
//       // draft.page.elements.insertAfter(undefined, newRect);
//
//       draft.page.elements.forEach((element, index) => {
//         console.log(
//           `Element ${index + 1}: Type=${element.type}, Position=${element.left}, ${element.top})`
//         );
//         elementsFound.push(element);
//         // element.left += 100;
//         // element.top += 100;
//       });
//       return await draft.save();
//     });
//     const result = await requestExport({
//       acceptedFileTypes: ['jpg'],
//     });
//     console.log(result)
//     if (result.status === "completed") {
//       result.exportBlobs.forEach((blob) => { console.log(blob.url) });
//       const imgUrl = result.exportBlobs[0].url;
//       const newIm = await upload({
//         type: "image",
//         mimeType: "image/jpeg",
//         url: imgUrl,
//         thumbnailUrl: imgUrl,
//         aiDisclosure: "app_generated",
//       });
//       await addElementAtPoint({
//         type: "image",
//         ref: newIm.ref,
//         altText: {
//           text: "example reuplaod",
//           decorative: false
//         },
//       });
//     }
//     console.log(elementsFound)
//   }
//
//   return (
//     <div className={styles.scrollContainer}>
//       <Rows spacing="2u">
//         <Button variant="primary" onClick={handleClick}>
//           Insert Rectangle</Button></Rows></div>
//   )
// }
export const getCanvaAuthorization = async () => {
  return new Promise<string | undefined>((resolve, reject) => {
    try {
      const url = new URL(endpoints.AUTHORIZE, process.env.BACKEND_URL);
      const windowFeatures = ["popup", "height=800", "width=800"];
      const authWindow = requestOpenExternalUrl({ url: PYTHON_BACKEND + "/authorize" })

      const checkAuth = async () => {
        try {
          const authorized = await checkForAccessToken();
          resolve(authorized.token);
        } catch (error) {
          reject(error);
        }
      };

      window.addEventListener("message", (event) => {
        if (event.data === "authorization_success") {
          checkAuth();
          authWindow?.close();
        } else if (event.data === "authorization_error") {
          reject(new Error("Authorization failed"));
          authWindow?.close();
        }
      });

      // Some errors from authorizing may not redirect to our servers,
      // in that case we need to check to see if the window has been manually closed by the user.
      const checkWindowClosed = setInterval(() => {
        if (authWindow?.closed) {
          clearInterval(checkWindowClosed);
          checkAuth();
        }
      }, 1000);
    } catch (error) {
      console.error("Authorization failed", error);
      reject(error);
    }
  });
};
export const TestPage = () => {
  function handleClick() {
  }

  const { userId } = useAppContext();
  const selection = useSelection("image")

  const processSelection = async () => {
    if (selection && selection.count > 0) {
      console.log(selection);
      console.log(selection.ref)
      const readselection = await selection.read();
      console.log(readselection)
      console.log(readselection.contents)
      console.log(readselection.contents[0].ref)
      const { url } = await getTemporaryUrl({ type: "image", ref: readselection.contents[0].ref })
      console.log(url)
    }
  }
  const hitBackend = async () => {
    const response = await fetch(PYTHON_BACKEND + "/carl");
    if (!response.ok) { console.log("didnt work") }
    const json = await response.json()
    console.log(json)
  }

  const exportDesignClick = async () => {
    const response = await fetch(PYTHON_BACKEND + `/api/get_design/${userId}`)
    const result = await response.json()
    console.log(result)
  }

  const AuthClick = async () => {
    const userToken = await auth.getCanvaUserToken();
    const designToken = await getDesignToken();

    const response = await fetch(PYTHON_BACKEND + `/my/api/endpoint/${designToken.token}`, {
      method: "POST", headers: {
        Authorization: `Bearer ${userToken}`
      }
    })

    const res = await response.json()

    console.log(res)
  }

  const AccessAuthClick = async () => {
    const link = await fetch(PYTHON_BACKEND + "/authorize")
    const url = await link.json()
    const req = await requestOpenExternalUrl({ url: url.url })
    console.log(req.status)
  }
  return (
    <div className={styles.scrollContainer}>
      <Rows spacing="2u">
        <Button variant="primary" onClick={() => hitBackend()}>
          Read design
        </Button>
        <Button variant="primary" onClick={() => processSelection()}>
          process selection
        </Button>
        <Button variant="primary" onClick={() => exportDesignClick()}>
          export design
        </Button>
        <Button variant="primary" onClick={() => AuthClick()}>
          Authorize
        </Button>
        <Button variant="primary" onClick={() => AccessAuthClick()}>
          Access Token
        </Button>
      </Rows>
    </div >
  )
}
