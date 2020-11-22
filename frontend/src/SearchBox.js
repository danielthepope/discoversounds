import React from 'react';
import AsyncSelect from 'react-select/async'

const SearchBox = ({ searchCallback }) => {
    const [artistQuery, setArtistQuery] = React.useState([]);
    const [searchBoxText, setSearchBoxText] = React.useState('');
    const [includeLocal, setIncludeLocal] = React.useState(true);

    const loadOptions = (inputValue, callback) => {
        if (inputValue.length > 1) {
            fetch(`/artists?term=${encodeURIComponent(inputValue)}`)
                .then(r => r.json())
                .then(j => callback(j))
                .catch(() => callback([]));
        } else {
            callback([]);
        }
    }

    const handleChange = (selectedItems) => {
        if (selectedItems) {
            const artistArray = selectedItems.map(i => i.value);
            setArtistQuery(artistArray);
        } else {
            setArtistQuery([]);
        }
    }

    const onInputChange = (thing) => {
        setSearchBoxText(thing);
    }

    const submitOnEnter = (e) => {
        if (e.key === 'Enter' && searchBoxText === '') {
            searchCallback(artistQuery, includeLocal);
        }
    }

    const customStyles = {
        valueContainer: (provided, state) => ({
            ...provided,
            cursor: 'text'
        }),
        multiValue: (provided, state) => ({
            ...provided,
            cursor: 'default'
        }),
        multiValueRemove: (provided, state) => ({
            ...provided,
            cursor: 'pointer'
        }),
    }

    // There are probably nicer ways to remove UI elements that I don't like, but hey.
    const DropdownIndicator = () => {
        return <></>;
    };

    const IndicatorSeparator = () => {
        return <></>;
    };

    return (
        <>
            <AsyncSelect
                className='search-box'
                components={{ DropdownIndicator, IndicatorSeparator }}
                loadOptions={loadOptions}
                onChange={handleChange}
                onInputChange={onInputChange}
                isMulti
                isClearable
                placeholder='Type artist names here'
                onKeyDown={submitOnEnter}
                styles={customStyles}
                theme={theme => ({
                    ...theme,
                    colors: {
                      ...theme.colors,
                      primary25: '#ffc8b4',
                      primary: '#ca3600',
                    },
                  })}
            />
            <div className='center'>
                <label htmlFor="includelocal">
                    <input type="checkbox" name="includelocal" id="includelocal"
                        onChange={e => setIncludeLocal(e.target.checked)} checked={includeLocal} />
                    Include local stations
                </label>
                <div className="inline">
                    <input
                        className="btn triggeranimation"
                        type="submit"
                        onClick={() => searchCallback(artistQuery, includeLocal)}
                        value="Search" />
                    {/* <input className="btn" type="submit" value="Play something now" name="redirect" /> */}
                </div>
            </div>
        </>
    );
};

export default SearchBox;