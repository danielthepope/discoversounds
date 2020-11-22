import React from 'react';

const Stats = () => {
    const [stats, setStats] = React.useState({});

    React.useEffect(() => {
        fetch('/stats')
            .then(r => r.json())
            .then(j => setStats(j));
    }, []);

    return (
        <p class="center"><small>
            <span class="separate inline">{stats.show_count} shows</span>
            <span class="separate inline">{stats.artist_count} artists</span>
            <span class="separate inline">Updated {stats.last_update}</span>
        </small></p>
    );
};

export default Stats;