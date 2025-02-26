import '../styles/Grid.css';
import PropTypes from 'prop-types';

function Grid({ nums, setNums }) {
  const handleCellClick = (index) => {
    const newValue = prompt('Enter a number (1-9) or 0 to clear:', nums[index]);
    if (newValue !== null && /^[0-9]$/.test(newValue)) {
      const newGrid = nums.split('');
      newGrid[index] = newValue;
      setNums(newGrid.join('')); // Updates the state in App
    }
  };

  return (
    <div className="grid-container">
      {nums.split('').map((num, index) => (
        <div 
          key={index} 
          className="grid-item" 
          onClick={() => handleCellClick(index)}
        >
          {num !== '0' ? num : ''}
        </div>
      ))}
    </div>
  );
}

Grid.propTypes = {
  nums: PropTypes.string.isRequired,
  setNums: PropTypes.func.isRequired,
};

export default Grid;

