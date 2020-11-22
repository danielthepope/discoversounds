import React from 'react';

const Result = ({ artists, availability_from, availability_to, image_url, other_artists, programmes_url, sid, sounds_url, synopsis, title, vpid }) => {
    const matchedArtists = artists.join(', ');
    const otherArtists = other_artists.join(', ');
    return (
        <>
        <hr/>
        <div className="result">
            <h3><a href={programmes_url}>{title}</a></h3>
            <div>
                <div className="left inline">
                    <a href={programmes_url}>
                        <img src={image_url} alt="" />
                    </a>
                </div>
                <div className="top inline">
                    <p>Broadcast on {availability_from} on {sid}</p>
                    <p>Matched artists: <strong>{matchedArtists}</strong></p>
                </div>
                <p>{synopsis}</p>
            </div>
            <details>
                <summary>Other artists played</summary>
                <p><small>{otherArtists}</small></p>
            </details>
        </div>
        </>
    );
};

export default Result;
