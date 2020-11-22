import SearchBox from './SearchBox';
import ResultsView from './ResultsView';
import Stats from './Stats';
import React from 'react';


function App() {
  const [results, setResults] = React.useState([]);

  const performSearch = (artists, includeLocal) => {
    const sanitisedArtists = artists.map(a => `artist=${encodeURIComponent(a)}`);
    fetch(`/search?${sanitisedArtists.join('&')}&includelocal=${includeLocal}`, {
      mode: "cors",
      headers: { 'Accept': 'application/json' }
    })
      .then(r => r.json())
      .then(json => setResults(json));
  }

  return (
    <>
      <h1><img className="icon" src="header-icon-small.jpg" alt="" /> Discover Sounds</h1>
      <div className='toSquash'>
        <p className='lead center'>Find shows on BBC Sounds you never knew existed.</p>
        <p className='center'>
          <small>
            <Stats />
          </small>
        </p>
      </div>
      <SearchBox searchCallback={performSearch} />
      <ResultsView results={results} />
      <hr />
      <div className="tofade">
        <h2>What is this?</h2>
        <p>This site indexes the shows that are available on <a href="https://www.bbc.co.uk/sounds">BBC Sounds</a>, along with the artists that were played on each.</p>
        <p>Choose your favourite artists and this service will find a radio show that plays most of them. The more artists you provide, the better the results will be.</p>
        <p>For example, if you submit The Strokes, Muse, Queens of the Stone Age and The White Stripes, you could get <a href="https://www.bbc.co.uk/programmes/m00021nz">this episode</a> of Radio 1's Indie Show back, which played all four of them.</p>
        <p>An <a href="https://github.com/danielthepope/discoversounds">open source project</a> created by <a href="https://twitter.com/danielthepope">Dan Pope</a> as part of a BBC hack day.</p>
      </div>
    </>
  );
}

export default App;
