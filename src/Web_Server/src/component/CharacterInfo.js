import React, { useState } from "react";
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import CheckBoxIcon from '@mui/icons-material/CheckBox';

import {
    Grid,
    Box,
    Card,
    Typography,
    CardContent,
    Paper,
    Button,
  } from "@mui/material";
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import { createTheme,ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#545454',
      darker: '#000000',
    },
    neutral: {
      main: '#ECECEC',
      contrastText: '#000000',
    },
  },
});


export default function CharacterInfo(props) {

    const [devices, setDevices] = React.useState(() => []);
    const [hairCheck, setHairCheck] = useState(false);
    const [hatCheck, setHatCheck] = useState(false);
    const [weaponCheck, setWeaponCheck] = useState(false);
    const [capeCheck, setCapeCheck] = useState(false);
    const [faceAccessoryCheck, setFaceAccessoryCheck] = useState(false);
    const [eyeAccessoryCheck, setEyeAccessoryCheck] = useState(false);
    const [eyeCheck, setEyeCheck] = useState(false);
    const [clothCheck, setClothCheck] = useState(false);






    let character_code = props.code
    console.log(character_code)
    const handleDevices = (
        event: React.MouseEvent<HTMLElement>,
        newDevices: string[],
    ) => {
        if (newDevices.length) {
        setDevices(newDevices);
        }
    };

  const inferSubmit = () => {
    //devices에 토클에 선택된 것들이 배열형태로 저장
    //예를 들어 무기랑 모자 선택하면 ['weapon','hat']
      console.log(hairCheck);
    }

  return (
      <Box
      sx={{
        p: 2, border: '1px dashed grey',
        borderRadius: '16px'
      }}
    >

    <Grid container spacing={2}>

      <Grid item xs={3}>
      <br/>
      <ThemeProvider theme={theme}>
      <Button color={hairCheck ? "neutral" : "error"}  variant="contained" component="label"
          onClick={() => {
            setHairCheck((e) => !e);
          }}
        >
          <h5>hair 아이템</h5>&ensp;
          <br/>
          {hairCheck ? <CheckBoxOutlineBlankIcon fontSize="small" /> : <CheckBoxIcon fontSize="small" />}
        </Button>
        </ ThemeProvider>

      <br/>
      <br/>
      <br/>
      <ThemeProvider theme={theme}>
      <Button color={eyeCheck ? "neutral" : "error"}  variant="contained" component="label"
          onClick={() => {
            setEyeCheck((e) => !e);
          }}
        >
          <h5>eye 아이템</h5>&ensp;
          <br/>
          {eyeCheck ? <CheckBoxOutlineBlankIcon fontSize="small" /> : <CheckBoxIcon fontSize="small" />}
        </Button>
        </ ThemeProvider>


      <br/>
      <br/>
      <br/>
      <ThemeProvider theme={theme}>
      <Button color={faceAccessoryCheck ? "neutral" : "error"}  variant="contained" component="label"
          onClick={() => {
            setFaceAccessoryCheck((e) => !e);
          }}
        >
          <h5>얼장 아이템</h5>&ensp;
          <br/>
          {faceAccessoryCheck ? <CheckBoxOutlineBlankIcon fontSize="small" /> : <CheckBoxIcon fontSize="small" />}
        </Button>
        </ ThemeProvider>

      <br/>
      <br/>
      <br/>
      <ThemeProvider theme={theme}>
      <Button color={eyeAccessoryCheck ? "neutral" : "error"}  variant="contained" component="label"
          onClick={() => {
            setEyeAccessoryCheck((e) => !e);
          }}
        >
          <h5>눈장 아이템</h5>&ensp;
          <br/>
          {eyeAccessoryCheck ? <CheckBoxOutlineBlankIcon fontSize="small" /> : <CheckBoxIcon fontSize="small" />}
        </Button>
        </ ThemeProvider>
      </Grid>

      <Grid item xs={6}>
    <Typography sx={{ mb: 1.5 }} color="text.secondary">
        <img src = {character_code.avatar_image}/>
    </Typography>
      <br/>
      <br/>
      <br/>
      <br/>
      <br/>
      <br/>

    <Typography variant="h5">
        캐릭터 이미지
    <br />
    <br />
    <ThemeProvider theme={theme}>
    <Button color="primary" variant="contained" onClick={inferSubmit}>추론하기</Button>
    </ ThemeProvider>

    </Typography>

      </Grid>
      <Grid item xs={3}>
      <br/>
      <ThemeProvider theme={theme}>
      <Button color={hatCheck ? "neutral" : "error"}  variant="contained" component="label"
          onClick={() => {
            setHatCheck((e) => !e);
          }}
        >
          <h5>hat 아이템</h5>&ensp;
          <br/>
          {hatCheck ? <CheckBoxOutlineBlankIcon fontSize="small" /> : <CheckBoxIcon fontSize="small" />}
        </Button>
        </ ThemeProvider>

      <br/>
      <br/>
      <br/>
      <ThemeProvider theme={theme}>
      <Button color={clothCheck ? "neutral" : "error"}  variant="contained" component="label"
          onClick={() => {
            setClothCheck((e) => !e);
          }}
        >
          <h5>옷 아이템</h5>&ensp;
          <br/>
          {clothCheck ? <CheckBoxOutlineBlankIcon fontSize="small" /> : <CheckBoxIcon fontSize="small" />}
        </Button>
        </ ThemeProvider>

      <br/>
      <br/>
      <br/>
      <ThemeProvider theme={theme}>
      <Button color={weaponCheck ? "neutral" : "error"}  variant="contained" component="label"
          onClick={() => {
            setWeaponCheck((e) => !e);
          }}
        >
          <h5>무기 아이템</h5>&ensp;
          <br/>
          {weaponCheck ? <CheckBoxOutlineBlankIcon fontSize="small" /> : <CheckBoxIcon fontSize="small" />}
        </Button>
        </ ThemeProvider>

      <br/>
      <br/>
      <br/>
      <ThemeProvider theme={theme}>
      <Button color={capeCheck ? "neutral" : "error"}  variant="contained" component="label"
          onClick={() => {
            setCapeCheck((e) => !e);
          }}
        >
          <h5>망토 아이템</h5>&ensp;
          <br/>
          {capeCheck ? <CheckBoxOutlineBlankIcon fontSize="small" /> : <CheckBoxIcon fontSize="small" />}
        </Button>
        </ ThemeProvider>
      </Grid>
    </Grid>
    </Box>

  );
}
