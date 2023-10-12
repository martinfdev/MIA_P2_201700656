import { PropTypes } from 'prop-types';

const Card = ({ name, imageUrl }) => {

    const openImageInNewTab = () => {
        window.open(imageUrl, '_blank');
    }
    return (
        <div className="max-w-xs rounded overflow-hidden shadow-md shadow-white transition-transform transform hover:scale-110 hover:bg-blue-950 p-1 border-2">
            <a href={imageUrl} target="_blank" rel='noopener noreferrer'>
                <img
                    src={imageUrl}
                    alt={name}
                    onClick={openImageInNewTab}
                    className="w-full h-full cursor-pointer" />
                <div className="flex p-4 justify-center">
                    <h2 className="font-bold text-lg text-white mb-2">{name}</h2>
                </div>
            </a>
        </div>
    );
}

Card.propTypes = {
    name: PropTypes.string.isRequired,
    imageUrl: PropTypes.string.isRequired
}

export default Card;