import { useState } from 'react'
import './App.css'
import Grid from './components/Grid';

function App() {
  const [img, setimg] = useState(null);
  const [nums, setNums] = useState(null);
  const API_BASE_URL = import.meta.env.VITE_API_URL;
  
  const handleSubmitParse = async () => {
    if (!img) {
      alert('Please select an image');
      return;
    }

    const formData = new FormData();
    formData.append('image', img);

    try {
      const response = await fetch(`${API_BASE_URL}/parse_img`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setNums(data.nums)
        console.log('Success:', data);
      } else {
        console.error('Error:', response.status);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleSubmitSolve = async () => {
    if (!nums) {
      alert('First Parse the Image');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/solve?puzzle=${nums}`, {
        method: 'GET',
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success == true) {
          setNums(data.solution);
        }
        console.log(data.solution)
        console.log('Success:', data);
      } else {
        console.error('Error:', response.status);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleClear = () =>{
    setNums(null);
    setimg(null);
  }

  return (
    <>
      <h1>Upload a Puzzle</h1>
      {img && (
        <div>
          <img
            alt='Sudoku Puzzle'
            width={"250px"}
            src={URL.createObjectURL(img)}
          />
          <br /> <br />
          <button onClick={handleClear}>Clear</button>
          <button onClick={handleSubmitParse}>Parse</button>
          {nums && (<button onClick={handleSubmitSolve}>Solve</button>)}
        </div>
      )}

      <br />
      
      {nums ? <h2>Click on a cell to edit the number</h2> : (
        <input
          type='file'
          name='sudokuImage'
          onChange={(event) => {
            console.log(event.target.files[0]);
            setimg(event.target.files[0]);
          }} />
      )}
      {nums && (
        <Grid nums={nums} setNums={setNums}/>
      )}
    </>

  )
}

export default App
