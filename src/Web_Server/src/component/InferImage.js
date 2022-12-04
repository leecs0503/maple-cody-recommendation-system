import React, { useState } from "react";
import CloseIcon from '@mui/icons-material/Close';
import {
  Dialog,
  ListItemText,
  ListItem,
  List,
  Divider,
  AppBar,
  Toolbar,
  IconButton,
  Slide,
  Box,
  Typography,
  Paper,
  Button,
} from "@mui/material";

import { TransitionProps } from '@mui/material/transitions';


const Transition = React.forwardRef(function Transition(
  props: TransitionProps & {
    children: React.ReactElement;
  },
  ref: React.Ref<unknown>,
) {
  return <Slide direction="up" ref={ref} {...props} />;
});


export default function CharacterInfo(props) {
  const [open, setOpen] = React.useState(false);
  let character_code = props.code
  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };


  return (
    <Box
      sx={{
        display: 'flex',
        flexWrap: 'wrap',
        '& > :not(style)': {
          m: 1,
          width: 1250,
          height: 300,
        },
      }}
    >
      <Paper elevation={3}>
      이미지 {props.image_name[0]}
      <br/>
      <br/>
    <Button variant="outlined" onClick={handleClickOpen}>
      상세 정보
    </Button>
    <Dialog
    fullScreen
    open={open}
    onClose={handleClose}
    TransitionComponent={Transition}
    >
    <AppBar sx={{ position: 'relative' }}>
      <Toolbar>
        <IconButton
          edge="start"
          color="inherit"
          onClick={handleClose}
          aria-label="close"
        >
          <CloseIcon />
        </IconButton>
        <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
          상세 정보
        </Typography>
      </Toolbar>
    </AppBar>
    <List>
    <ListItem>
      <ListItem button>
        <ListItemText primary="모자" secondary="정열적인 모자, 가격 만원" />
        <img src = {character_code.avatar_image}/>
      </ListItem>
      </ListItem>
      <Divider />
      <ListItem>
      <ListItem button>
        <ListItemText primary="무기" secondary="정열적인 무기, 가격 만원" />
        <img src = {character_code.avatar_image}/>
      </ListItem>
      </ListItem>
      <Divider />
      <ListItem>
      <ListItem button>
        <ListItemText primary="옷" secondary="정열적인 옷, 가격 만원" />
        <img src = {character_code.avatar_image}/>
      </ListItem>
      </ListItem>
    </List>
    </Dialog>

      </Paper>
      <Paper elevation={3}>
      이미지  {props.image_name[1]}
      </Paper>
    </Box>
  );
}
