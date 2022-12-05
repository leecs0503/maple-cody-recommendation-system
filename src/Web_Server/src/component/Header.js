import './Header.css'
import Grid from '@mui/material/Grid';
import { Typography, Box } from '@mui/material';

export default function Header() {
  return (
    <Box className="top-nav" 
      sx={{borderBottom: 0.5, borderColor: "#CCCCCC"}}    
      style={{
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
      }}
    >

      <Grid container >
        <Grid xs={1} />
        <Grid xs={10} style={{
          "display": "flex",
          "alignItems": "center",
          "justifyContent": "center",
        }}>
          <Typography
            variant="h5"
            fontFamily="inter-extra-bold"
          >
            Korea University COSE489 Final Project - Team 4
          </Typography>
        </Grid>
        <Grid xs={1} />
      </Grid>

    </Box>
  );
}
