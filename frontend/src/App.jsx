import { useState } from 'react'
import './App.css'
import Grid from './components/Grid';

function App() {
  const [img, setimg] = useState(null);
  const [nums, setNums] = useState(null);
  
  const handleSubmit = async () => {
    if (!img) {
      alert('Please select an image');
      return;
    }

    const formData = new FormData();
    formData.append('image', img);

    try {
      const response = await fetch('http://localhost:5000/parse_img', {
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

  return (
    <>
      <h1>Upload a Puzzle</h1>
      {img && (
        <div>
          <img
            alt='not found'
            width={"250px"}
            src={URL.createObjectURL(img)}
          />
          <br /> <br />
          <button onClick={() => setimg(null)}>Remove</button>
          <button onClick={handleSubmit}>Solve</button>
        </div>
      )}

      <br />

      <input
        type='file'
        name='sudokuImage'
        onChange={(event) => {
          console.log(event.target.files[0]);
          setimg(event.target.files[0]);
        }} />
      {nums && (
        <Grid nums={nums}/>
      )}
    </>

  )
}

export default App
