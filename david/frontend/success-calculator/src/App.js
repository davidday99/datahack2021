import React, { useState } from 'react';
import Container from '@material-ui/core/Container';
import Card from '@material-ui/core/Card';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';
import { Button, CardContent, FormControlLabel, Typography } from '@material-ui/core';
import Radio from '@material-ui/core/Radio';
import axios from 'axios';
 

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
  const [artistName, setArtistName] = useState('');
  const [songName, setSongName] = useState('');
  const [albumName, setAlbumName] = useState('');

  const [beatsPerMeasure, setBeatsPerMeasure] = useState(0);
  const [beatsPerMinute, setBeatsPerMinute] = useState(0);
  const [lengthInMinutes, setLengthInMinutes] = useState(0);
  const [lyricism, setLyricism] = useState(0);
  const [volume, setVolume] = useState(0);

  const [danceability, setDanceability] = useState(0);
  const [positivity, setPositivity] = useState(0);
  const [hype, setHype] = useState(0);
  const [instrumentalness, setInstrumentalness] = useState(0);

  const [vulgarity, setVulgarity] = useState(false) // false = not vulgar, true = vulgar
  const [concertProbability, setConcertProbability] = useState(0);

  const [auditory, setAuditory] = useState(0)
  const [majorMinor, setMajorMinor] = useState(false) // false = minor, true = major

  const [styles, setStyles] = useState('rock') // default to rock
  const [tone, setTone] = useState('C') // default to C

  // const keys = ['C#', 'D', 'F', 'C', 'E', 'A', 'B', 'Bb', 'Ab', 'G', 'F#', 'D#']



  function errorCheckStringToInt(value) {
    let ret = 0
    try {
      ret = parseInt(value)
    }
    catch(error) {
      console.log(error)
    }
    return ret;
  }

  function errorCheckStringToFloat(value) {
    let ret = 0
    try {
      ret = parseFloat(value)
    }
    catch(error) {
      console.log(error)
    }
    return ret;
  }

  function postData() {
      const data = {
          artist: artistName,
          name: songName,
          album: albumName,
          beats_per_measure: beatsPerMeasure,
          beats_per_min: beatsPerMinute,
          length_minutes: lengthInMinutes,
          lyricism: lyricism,
          volume: volume,
          danceability: danceability,
          positivity: positivity,
          hype: hype,
          instrumentalness: instrumentalness,
          styles: styles,
          'major/minor': majorMinor ? 'major' : 'minor',
          vulgar: vulgarity ? 'VULGAR' : 'NOT VULGAR',
          concert_probability: concertProbability,
          auditory: auditory,
          tone: tone
      }
      console.log(data)
      axios.post('http://127.0.0.1:5000/api/model1', data)
  }

  return (
    <Container style={{textAlign: 'center'}}>
      <h1>Is this your next hit?</h1>
      <Card style={{margin: '10px', minHeight:500}}>
            <form className={classes.root}>
                <div>
                    <CardContent>
                        <Typography variant="h5">
                        General Info
                        </Typography>
                    </CardContent>
                  
                    <TextField required id="standard-required" label="Artist Name" onChange={event => setArtistName(event.target.value)}/>
                    <TextField required id="standard-required" label="Song Name" onChange={event => setSongName(event.target.value)}/>
                    <TextField required id="standard-required" label="Album Name" onChange={event => setAlbumName(event.target.value)}/>

                    <br/>
                    <br/>
                    
                    <CardContent>
                        <Typography variant="h5">
                        Song Properties
                        </Typography>
                    </CardContent>

                    <TextField
                    id="standard-number"
                    label="Beats per Measure"
                    type="number"
                    InputLabelProps={{
                        shrink: true,
                    }}
                    onChange={event => setBeatsPerMeasure(errorCheckStringToInt(event.target.value))}
                    />
                     <TextField
                    id="standard-number"
                    label="Beats per Minute"
                    type="number"
                    InputLabelProps={{
                        shrink: true,
                    }}
                    onChange={event => setBeatsPerMinute(errorCheckStringToInt(event.target.value))}
                    />
                     <TextField
                    id="standard-number"
                    label="Length in Minutes"
                    type="number"
                    InputLabelProps={{
                        shrink: true,
                    }}
                    onChange={event => setLengthInMinutes(errorCheckStringToInt(event.target.value))}
                    />
                    <TextField
                    id="standard-number"
                    label="Auditory"
                    type="number"
                    InputLabelProps={{
                        shrink: true,
                    }}
                    onChange={event => setAuditory(errorCheckStringToFloat(event.target.value))}
                    />
                    <TextField
                    id="standard-number"
                    label="Lyricism"
                    type="number"
                    InputLabelProps={{
                        shrink: true,
                    }}
                    onChange={event => setLyricism(errorCheckStringToFloat(event.target.value))}
                    />
                    <TextField
                    id="standard-number"
                    label="Volume"
                    type="number"
                    InputLabelProps={{
                        shrink: true,
                    }}
                    onChange={event => setVolume(errorCheckStringToFloat(event.target.value))}
                    />

                    <TextField id="standard-required" label="Danceability" onChange={event => setDanceability(errorCheckStringToFloat(event.target.value))}/>
                    <TextField id="standard-required" label="Positivity" onChange={event => setPositivity(errorCheckStringToFloat(event.target.value))}/>
                    <TextField id="standard-required" label="Hype" onChange={event => setHype(errorCheckStringToFloat(event.target.value))}/>
                    <TextField id="standard-required" label="Instrumentalness" onChange={event => setInstrumentalness(errorCheckStringToFloat(event.target.value))}/>
                    <TextField id="standard-required" label="Style" onChange={event => setStyles(event.target.value)}/>

                    <CardContent>
                        <Typography variant="h5">
                        Tone
                        </Typography>
                    </CardContent>
                    
                    <FormControlLabel
                    checked={majorMinor}
                    control={<Radio color="primary" />}
                    label="Major"
                    labelPlacement="top"
                    onChange={event => setMajorMinor(true)}
                    />

                    <FormControlLabel
                    checked={!majorMinor}
                    control={<Radio color="primary" />}
                    label="Minor"
                    labelPlacement="top"
                    onChange={event => setMajorMinor(false)}
                    />
                    
                    <br/>


                    {/* <Slider
                    style={{maxWidth: 200}}
                    defaultValue={20}
                    getAriaValueText={valuetext}
                    onChange={event => console.log(event.target.value)}
                    aria-labelledby="discrete-slider-custom"
                    step={10}
                    valueLabelDisplay="auto"
                    marks={keys}
                    /> */}

                    <TextField required id="standard-required" label="Key" onChange={event => setTone(event.target.value)}/>

                    <CardContent>
                        <Typography variant="h5">
                        Vulgarity
                        </Typography>
                    </CardContent>
                    
                    <FormControlLabel
                    checked={vulgarity}
                    control={<Radio color="primary" />}
                    label="Yes"
                    labelPlacement="top"
                    onChange={event => setVulgarity(true)}
                    />

                    <FormControlLabel
                    checked={!vulgarity}
                    control={<Radio color="primary" />}
                    label="No"
                    labelPlacement="top"
                    onChange={event => setVulgarity(false)}
                    /> 

                    <CardContent>
                        <Typography variant="h5">
                        Misc.
                        </Typography>
                    </CardContent>

                    <TextField required id="standard-required" label="Concert Probability" onChange={event => setConcertProbability(errorCheckStringToFloat(event.target.value))}/>


                </div>
                <br/>
                <Button onClick={postData}>Calculate</Button>
                <br/>
                <br/>
            </form>
        </Card>
      <h1>Projected Streams</h1>
      <Card>
        <CardContent>
          -
        </CardContent>
      </Card>
      <h1>Sample Review</h1>
      <Card>
        <CardContent>
          -
        </CardContent>
      </Card>
      <br/>
    </Container>
  );
}

export default App;
