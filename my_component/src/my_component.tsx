import React from "react";
import { withStreamlitConnection, Streamlit } from "streamlit-component-lib";

function MyComponent() {
  return (
    <div>
      <button onClick={() => Streamlit.setComponentValue("Hello from JS")}>點我送資料</button>
    </div>
  );
}

export default withStreamlitConnection(MyComponent);