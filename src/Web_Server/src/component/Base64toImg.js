const Base64toImg = (
  {
    imageData,
    width,
    height
  }
) => {
  return (
    < img
      style={{
        width, height, zIndex: 2
      }}
      src={`data:image/jpeg;base64,${imageData}`}
    />
  )
}
export default Base64toImg