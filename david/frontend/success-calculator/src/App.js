import React from 'react';
import Container from '@material-ui/core/Container';
import Card from '@material-ui/core/Card';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';
import { Button, CardContent } from '@material-ui/core';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';

const useStyles = makeStyles((theme) => ({
  root: {
    '& .MuiTextField-root': {
      margin: theme.spacing(1),
      width: '25ch',
    },
  },
}));

function App() {
  const classes = useStyles();
  return (
    <Container style={{textAlign: 'center'}}>
      <h1>Is this your next hit?</h1>
      <Card style={{margin: '10px', minHeight:500}}>
            <form className={classes.root}>
                <div>
                    <TextField required id="standard-required" label="Artist Name"/>
                    <TextField required id="standard-required" label="Song Name"/>
                    <TextField required id="standard-required" label="Album Name"/>
                    <TextField
                    id="standard-number"
                    label="Beats per Measure"
                    type="number"
                    InputLabelProps={{
                        shrink: true,
                    }}
                    />
                     <TextField
                    id="standard-number"
                    label="Beats per Minute"
                    type="number"
                    InputLabelProps={{
                        shrink: true,
                    }}
                    />
                     <TextField
                    id="standard-number"
                    label="Length in Minutes"
                    type="number"
                    InputLabelProps={{
                        shrink: true,
                    }}
                    />
                    <TextField
                    id="standard-number"
                    label="Lyricism"
                    type="number"
                    InputLabelProps={{
                        shrink: true,
                    }}
                    />
                    <TextField
                    id="standard-number"
                    label="Volume"
                    type="number"
                    InputLabelProps={{
                        shrink: true,
                    }}
                    />
                    <TextField id="standard-required" label="Concert Probability"/>
                    <TextField id="standard-required" label="Danceability"/>
                    <TextField id="standard-required" label="Hype"/>
                    <TextField id="standard-required" label="Instrumentalness"/>
                    <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    >
                    <MenuItem>Ten</MenuItem>
                    <MenuItem>Twenty</MenuItem>
                    <MenuItem>Thirty</MenuItem>
                    </Select>

                </div>
                <Button type="submit">Calculate</Button>
            </form>
        </Card>
      <h1>Projected Streams</h1>
      <Card>
        <CardContent>
          Test
        </CardContent>
      </Card>
      <h1>Sample Review</h1>
      <Card>
        <CardContent>
          Test
        </CardContent>
      </Card>
    </Container>
  );
}

export default App;
