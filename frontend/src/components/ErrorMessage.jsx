import React from 'react'

const ErrorMessage = ({message}) => {
  return (
    <p className="has-text-bold has-text-danger">
    {message}
    </p>
  )
}

export default ErrorMessage