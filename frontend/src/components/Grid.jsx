import '../styles/Grid.css'; // Import the CSS file
import PropTypes from 'prop-types';

function Grid({nums}) {

  if (nums.length !== 81) {
    return <div>Error: nums must be a string of length 81.</div>;
  }

  const gridItems = Array.from({ length: 81 }, (_, index) => (
    <div key={index} className="grid-item">{nums[index] != 0 ? nums[index] : ''}</div>
  ));

  return (
    <div className="grid-container">
      {gridItems}
    </div>
  );
}

Grid.propTypes = {
  nums: PropTypes.string.isRequired,
}

export default Grid;
