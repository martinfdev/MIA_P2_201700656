import { useState } from "react"
import { PropTypes } from "prop-types"

function TextArea({ value, onChange, isEditable }) {
    // eslint-disable-next-line no-unused-vars
    const [text, setText] = useState("")

    const handleTextChange = (event) => {
        const newText = event.target.value
        setText(newText)
        onChange(newText)
    }
    return (
        <div className="flex h-1/2 w-full">
            <textarea
                name="text area"
                className="h-full w-full bg-slate-500 text-white font-bold border-2 hover:border-warning p-3 resize-none"
                value={value}
                onChange={handleTextChange}
                readOnly={isEditable ? false : true}
                autoCorrect="off"
            />
        </div>
    )
}

TextArea.propTypes = {
    value: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    isEditable: PropTypes.bool
}
export default TextArea