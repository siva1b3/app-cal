import "./App.css";

function App() {
  return (
    <main
      style={{
        width: "95vw",
        height: "95vh",
        margin: 0,
        padding: 0,
        display: "flex",
        flexDirection: "column",
        backgroundColor: "lightskyblue",
      }}
    >
      <div style={{ flex: 1, backgroundColor: "lightcoral" }}>
        <h1 style={{ textAlign: "center", color: "white" }}>Section 1</h1>
      </div>
      <div style={{ flex: 1, backgroundColor: "lightblue" }}>
        <h1 style={{ textAlign: "center", color: "white" }}>Section 2</h1>
      </div>
      <div style={{ flex: 1, backgroundColor: "lightgreen" }}>
        <h1 style={{ textAlign: "center", color: "white" }}>Section 3</h1>
      </div>
      <div style={{ flex: 1, backgroundColor: "goldenrod" }}>
        <h1 style={{ textAlign: "center", color: "white" }}>Section 4</h1>
      </div>
    </main>
  );
}

export default App;
