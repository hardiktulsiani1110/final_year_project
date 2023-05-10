// import logo from './logo.svg';
import React, { useState, useEffect } from "react";
import "./App.css";
import { Link } from "react-router-dom";

function App() {
  let [items, setItems] = useState([]);
  let [items2, setItems2] = useState([]);
  let [items3, setItems3] = useState([]);
  let [items4, setItems4] = useState([]);
  let [items5, setItems5] = useState([]);

  const [formData, setFormData] = useState({
    user: "",
    query1: "",
  });
  let [key, setKey] = useState("");
  // useEffect(() => {
  //   getItems();
  //   getItems2();
  //   getItems3();
  // }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log(formData);

    // getOnlyArticles();
    //fetch req goes here

    if (formData.user === "article") {
      console.log("Articles");
      setItems5([]);
      setItems3([]);
      setItems2([]);
      setItems([]);
      getOnlyArticles();
      //send keywords request
    } else if (formData.user === "section") {
      console.log("Sections");
      setItems4([]);
      setItems3([]);
      setItems2([]);
      setItems([]);
      getOnlySections();
      //send section request
    } else {
      console.log("Keywords");
      //send articles request
      setItems5([]);
      setItems4([]);
      getItems();
      getItems2();
      getItems3();
    }
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;

    setFormData({ ...formData, [name]: value });
  };

  let getItems = async () => {
    // let response = await fetch("http://127.0.0.1:8000/api/notes");
    let response, data;
    response = await fetch("http://127.0.0.1:8000/api/keywords/", {
      method: "POST",
      body: JSON.stringify({
        // keyword: "services",
        statement: formData.query1,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    data = await response.json();
    // console.log("data", data);
    // setKey(data?.keyword);
    setItems(data);
    // console.log("variable", data);
    // setItems(data);
    // func(items);
  };

  let func = (items) => {
    let arr = [];
    for (var i = 0; i < items.length; i++) {
      arr.push(<div>{items[i]}</div>);
    }
    console.log("ITEMS UPDATES");
    return arr;
  };

  let getItems2 = async () => {
    // let response = await fetch("http://127.0.0.1:8000/api/notes");
    let response2, data2;
    console.log(formData.query1);

    response2 = await fetch("http://127.0.0.1:8000/api/sections/", {
      method: "POST",
      body: JSON.stringify({
        // keyword: "services",
        statement: formData.query1,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    data2 = await response2.json();
    // console.log("data", data);
    // setKey(data?.keyword);
    setItems2(data2);
    console.log("sections", data2);
    // func2(items2);
    // setItems(data);
  };

  let func2 = (items2) => {
    let arr2 = [];
    for (var i = 0; i < items2.length; i++) {
      arr2.push(<div>{items2[i]}</div>);
    }
    console.log("ITEMS UPDATES 2");
    return arr2;
  };

  let getItems3 = async () => {
    // let response = await fetch("http://127.0.0.1:8000/api/notes");
    let response3, data3;
    response3 = await fetch("http://127.0.0.1:8000/api/articles/", {
      method: "POST",
      body: JSON.stringify({
        // keyword: "services",
        statement: formData.query1,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    data3 = await response3.json();
    // console.log("data", data);
    // setKey(data?.keyword);
    setItems3(data3);
    console.log("data for articles", data3);
    // setItems(data);
  };

  let func3 = (items3) => {
    let arr3 = [];
    for (var i = 0; i < items3.length; i++) {
      arr3.push(<div>{items3[i]}</div>);
    }
    console.log("ITEMS UPDATES 3");
    return arr3;
  };

  let getOnlyArticles = async () => {
    let response = await fetch("http://127.0.0.1:8000/api/onlyarticles/", {
      method: "POST",
      body: JSON.stringify({
        // keyword: "services",
        statement: formData.query1,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    let tempdata = await response.json();
    setItems4(tempdata);
    console.log("only articles", tempdata);
  };

  let getOnlySections = async () => {
    let response = await fetch("http://127.0.0.1:8000/api/onlysections/", {
      method: "POST",
      body: JSON.stringify({
        // keyword: "services",
        statement: formData.query1,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    let tempdata1 = await response.json();
    setItems5(tempdata1);
    console.log("only sections", tempdata1);
  };

  // if (items.length === 0) {
  //   return <div className="App">app</div>;
  // }
  // return <div className="App">{items.length !== 0 && items?.body}</div>;

  return (
    <div className="App">
      <header class="header-fixed">
        <div class="header-limiter">
          <h1>
            <a href="#">Legal Data Mining</a>
          </h1>
        </div>
      </header>

      <div class="header-fixed-placeholder"></div>

      <form onSubmit={handleSubmit}>
        <div className="sect">
          <label htmlFor="user">Choose the type of User:</label>
          <select
            id="user"
            name="user"
            className="select-container"
            value={formData.user}
            onChange={handleInputChange}
          >
            <option value="keywords">Keywords</option>
            <option value="section">Section</option>
            <option value="article">Article</option>
          </select>
        </div>

        <label htmlFor="query">Enter your query:</label>
        <input
          type="text"
          id="query1"
          name="query1"
          placeholder="Enter search terms..."
          value={formData.query1}
          onChange={handleInputChange}
        />
        <button className="search" type="submit">
          Search
        </button>
      </form>

      <section id="results">
        {/* <h2>Results</h2> */}
        <table style={{ width: "100%" }}>
          <tr>
            <td style={{ width: "15%", backgroundColor: "#ccc" }}>
              <h2>Case Number</h2>
            </td>
            <td style={{ width: "15%", backgroundColor: "#eee" }}>
              <h2>Date</h2>
            </td>
            <td style={{ width: "70%", backgroundColor: "#ccc" }}>
              <h2>Link for Case</h2>
            </td>
          </tr>
        </table>

        <table style={{ width: "100%" }}>
          {items.length > 0 && <tr>Keywords</tr>}
          {items.map((i) => (
            <tr>
              <td style={{ width: "15%", backgroundColor: "#ccc" }}>
                <p>{i.number}</p>
              </td>
              <td style={{ width: "15%", backgroundColor: "#eee" }}>
                <p>{i.date}</p>
              </td>
              <td style={{ width: "70%", backgroundColor: "#ccc" }}>
                <a href={i.url} target="_blank" rel="noopener noreferrer">
                  {i.url}{" "}
                </a>
              </td>
            </tr>
          ))}
          {items2.length > 0 && <tr>Sections</tr>}
          {items2.map((i) => (
            <tr>
              <td style={{ width: "15%", backgroundColor: "#ccc" }}>
                <p>{i.number}</p>
              </td>
              <td style={{ width: "15%", backgroundColor: "#eee" }}>
                <p>{i.date}</p>
              </td>
              <td style={{ width: "70%", backgroundColor: "#ccc" }}>
                <a href={i.url} target="_blank" rel="noopener noreferrer">
                  {i.url}{" "}
                </a>
              </td>
            </tr>
          ))}
          {items3.length > 0 && <tr>Articles</tr>}
          {items3.map((i) => (
            <tr>
              <td style={{ width: "15%", backgroundColor: "#ccc" }}>
                <p>{i.number}</p>
              </td>
              <td style={{ width: "15%", backgroundColor: "#eee" }}>
                <p>{i.date}</p>
              </td>
              <td style={{ width: "70%", backgroundColor: "#ccc" }}>
                <a href={i.url} target="_blank" rel="noopener noreferrer">
                  {i.url}{" "}
                </a>
              </td>
            </tr>
          ))}
          {items4.length > 0 && <tr>Articles</tr>}
          {items4.map((i) => (
            <tr>
              <td style={{ width: "15%", backgroundColor: "#ccc" }}>
                <p>{i.number}</p>
              </td>
              <td style={{ width: "15%", backgroundColor: "#eee" }}>
                <p>{i.date}</p>
              </td>
              <td style={{ width: "70%", backgroundColor: "#ccc" }}>
                <a href={i.url} target="_blank" rel="noopener noreferrer">
                  {i.url}{" "}
                </a>
              </td>
            </tr>
          ))}
          {items5.length > 0 && <tr>Sections</tr>}
          {items5.map((i) => (
            <tr>
              <td style={{ width: "15%", backgroundColor: "#ccc" }}>
                <p>{i.number}</p>
              </td>
              <td style={{ width: "15%", backgroundColor: "#eee" }}>
                <p>{i.date}</p>
              </td>
              <td style={{ width: "70%", backgroundColor: "#ccc" }}>
                <a href={i.url} target="_blank" rel="noopener noreferrer">
                  {i.url}{" "}
                </a>
              </td>
            </tr>
          ))}{" "}
        </table>

        {/* <table style={{ width: "100%" }}>
          <tr>
            <td style={{ width: "15%", backgroundColor: "#ccc" }}>
              <h2>Case Number</h2>
              <td>
                {" "}
                <p>This is the content for column 1.</p>
              </td>
            </td>
            <td style={{ width: "15%", backgroundColor: "#eee" }}>
              <h2>Date</h2>
              <td>
                {" "}
                <p>This is the content for column 2.</p>
              </td>
            </td>
            <td style={{ width: "70%", backgroundColor: "#ccc" }}>
              <h2>Link for Case</h2>
              <td>
                {" "}
                <p>This is the content for column 3.</p>
              </td>
            </td>
          </tr>

          <tr>
            {items.map((i) => (
              <div>
                number:{i.number} date:{i.date} url:{i.url}
              </div>
            ))}
          </tr>

          <br></br>
          <tr>
            {items2.map((i) => (
              <div>
                number:{i.number} date:{i.date} url:{i.url}
              </div>
            ))}
          </tr>

          <br></br>
          <tr>
            {items3.map((i) => (
              <div>
                number:{i.number} date:{i.date} url:{i.url}
              </div>
            ))}
          </tr>
        </table> */}
      </section>

      <div className="footer">
        <div className="F1">
          <div>
            <p>Made By :-</p>
            <p>
              Hardik Tulsiani, Hiren Dhadhal, Aramya Maheshwari, Utsav chordia
            </p>
          </div>
          <div>
            <p>Guided By :- Dr. Dipti P Rana</p>
          </div>
        </div>
      </div>
      {/* {func(items)} */}
    </div>
  );
}

export default App;
