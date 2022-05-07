import React, { useEffect, useState } from 'react'
import Header from './components/Header';
import Register from './components/Register';
const App = () => {
  const [message,setMessage] = useState("");

  const getWelcomeMessage = async() =>{
    const requestOptions = {
      method:"GET",
      headers:{
        "Content-Type":"application.json"
      },
    }
    const response = await fetch('/api',requestOptions)
    const data = await response.json(); 

    if (!response.ok){
      alert ("No message to display")
    } else{
      setMessage(data.message);
    }
  };

  useEffect(()=>{
    getWelcomeMessage();
  },[]);

  return (
    <>
    <Header title={message}/>
    <Register/>
    </>
  )
};

export default App