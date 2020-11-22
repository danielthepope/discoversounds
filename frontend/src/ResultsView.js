import React from 'react';
import Result from './Result';

const ResultsView = ({results}) => {
    console.log('results', results)
    const allResults = results.map(r => <Result {...r} />);
    return (
        <div>
            {allResults}
        </div>
    );
};

export default ResultsView;