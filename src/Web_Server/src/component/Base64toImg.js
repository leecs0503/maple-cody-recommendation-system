const Base64toImg = (
  {
    imageData,
    // boxSize,
  }
) => {
  return (
    < img
      // boxSize={boxSize}
      src={`data:image/jpeg;base64,${imageData}`}
    />
  )
}
export default Base64toImg