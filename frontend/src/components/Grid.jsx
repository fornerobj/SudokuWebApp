import '../styles/Grid.css';
import PropTypes from 'prop-types';
import { useState } from 'react';

function Grid({ nums, setNums }) {
  const [selectedCell, setSelectedCell] = useState(null);

  const handleCellClick = (index) => {
    setSelectedCell(index)
  };

  const handleNumberClick = (number) => {
    if (selectedCell !== null) {
      const newGrid = nums.split('');
      newGrid[selectedCell] = number.toString();
      setNums(newGrid.join(''));
      setSelectedCell(null);
    }
  };

  const handleCloseNumpad = () => {
    setSelectedCell(null);
  }

  return (
    <div className='sudoku-area'>
      <div className="grid-container">
          {nums.split('').map((num, index) => {
          const row = Math.floor(index / 9);
          const col = index % 9;
          const boxRow = Math.floor(row / 3);
          const boxCol = Math.floor(col / 3);
          const isBottomBorder = row % 3 === 2 && row < 8;
          const isRightBorder = col % 3 === 2 && col < 8;
          
          return (
            <div 
              key={index} 
              className={`grid-item ${selectedCell === index ? 'selected' : ''} ${
                isBottomBorder ? 'bottom-border' : ''
              } ${
                isRightBorder ? 'right-border' : ''
              }`}
              onClick={() => handleCellClick(index)}
            >
              {num !== '0' ? num : ''}
            </div>
          );
        })}
      </div>
      {selectedCell !== null && (
        <div className="numpad-overlay">
          <div className="numpad-container">
            <div className="numpad-header">
              <h3>Select a number</h3>
              <button className="close-button" onClick={handleCloseNumpad}>×</button>
            </div>
            <div className="numpad">
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 0].map((number) => (
                <button 
                  key={number} 
                  className="numpad-button"
                  onClick={() => handleNumberClick(number)}
                >
                  {number === 0 ? 'Clear' : number}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

Grid.propTypes = {
  nums: PropTypes.string.isRequired,
  setNums: PropTypes.func.isRequired,
};

export default Grid;

