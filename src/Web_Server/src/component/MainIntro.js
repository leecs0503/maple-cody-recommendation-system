import './MainIntro.css';
import GitHubIcon from '@mui/icons-material/GitHub';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';

import Grid from '@mui/material/Grid';
import { Typography, Box, Button, IconButton } from '@mui/material';
import { Fragment } from "react";

const theme = createTheme({
  palette: {
    primary: {
      main: '#0971f1',
      darker: '#053e85',
    },
    neutral: {
      main: '#ECECEC',
      contrastText: '#000000',
    },
  },
});

export default function MainIntro() {
  const navigate = useNavigate();
  const GitHubUrl = 'https://github.com/leecs0503/maple-cody-recommendation-system';
  const GitHubSubmit = () => {
    window.location.replace(GitHubUrl);
  }

  return (
    <Fragment>
      <Box style={{
        "paddingTop": "7.5vh",
      }}>
        <div className="top-nav" style={{
          "display": "flex",
          "alignItems": "center",
          "justifyContent": "center",
          width: '100vw'
        }}>
          <Typography
            variant="h3"
            fontFamily="inter-extra-bold"
            color="#e53e3e"
          >
            Maplestory&nbsp;
          </Typography>
          <Typography
            variant="h3"
            fontFamily="inter-extra-bold"
          >
            Cody Recommand Site
          </Typography>
        </div>
        <div className="top-nav" style={{
          "display": "flex",
          "alignItems": "center",
          "justifyContent": "center",
          width: '50vw',
          paddingLeft: '25vw',
          paddingTop: '5vh',

        }}>
          고려대학교 캡스톤 디자인 (COSE489) Team 4의 Final Project Page입니다.
          <br />
          기존의 캐릭터 코디로부터 이미지 인식 기반 딥러닝 모델을 통해 코디 추천을 진행합니다.
        </div>
        <div className="top-nav" style={{
          "display": "flex",
          "alignItems": "center",
          "justifyContent": "center",
          width: '70vw',
          paddingLeft: '14.5vw',
          paddingTop: '3vh',
          paddingBottom: '5vh',
        }}>

          <Button color="error" variant="contained" component="label" size="large" onClick={GitHubSubmit} >
            <GitHubIcon />
            &nbsp;&nbsp;GitHub
          </Button>
          &nbsp;&nbsp;&nbsp;&nbsp;
          <ThemeProvider theme={theme}>
            <Button color="neutral" variant="contained" component="label" size="large">
              &ensp;&ensp;PaPer&ensp;&ensp;
            </Button>
          </ThemeProvider>
        </div>
      </Box>
    </Fragment>
  );
}
