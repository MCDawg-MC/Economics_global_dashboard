import React, { useState, useEffect } from 'react';
import Map, { Source, Layer, Popup } from 'react-map-gl';
import { getMapData } from '../services/api';
import './MomentumMap.css';

const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN;

function MomentumMap({ includeStructural = false, onCountryClick }) {
  const [mapData, setMapData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [popupInfo, setPopupInfo] = useState(null);

  const [viewState, setViewState] = useState({
    longitude: 0,
    latitude: 20,
    zoom: 1.5
  });

  useEffect(() => {
    loadMapData();
  }, [includeStructural]);

  const loadMapData = async () => {
    try {
      setLoading(true);
      const data = await getMapData(includeStructural);
      setMapData(data);
      setError(null);
    } catch (err) {
      setError('Failed to load map data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleClick = (event) => {
    const feature = event.features && event.features[0];
    if (feature) {
      const props = feature.properties;
      setPopupInfo({
        longitude: feature.geometry.coordinates[0],
        latitude: feature.geometry.coordinates[1],
        ...props
      });
    }
  };

  const handleCountrySelect = () => {
    if (popupInfo && onCountryClick) {
      onCountryClick(popupInfo.country_code);
    }
  };

  if (loading) {
    return <div className="map-loading">Loading map...</div>;
  }

  if (error) {
    return <div className="map-error">{error}</div>;
  }

  if (!MAPBOX_TOKEN) {
    return (
      <div className="map-error">
        Mapbox token not configured. Please add REACT_APP_MAPBOX_TOKEN to your .env file.
      </div>
    );
  }

  return (
    <div className="map-container">
      <Map
        {...viewState}
        onMove={evt => setViewState(evt.viewState)}
        mapStyle="mapbox://styles/mapbox/light-v11"
        mapboxAccessToken={MAPBOX_TOKEN}
        onClick={handleClick}
        interactiveLayerIds={['country-points']}
      >
        {mapData && (
          <Source id="countries" type="geojson" data={mapData}>
            <Layer
              id="country-points"
              type="circle"
              paint={{
                'circle-radius': [
                  'interpolate',
                  ['linear'],
                  ['zoom'],
                  1, 5,
                  5, 15
                ],
                'circle-color': ['get', 'color'],
                'circle-opacity': 0.8,
                'circle-stroke-width': 2,
                'circle-stroke-color': '#fff'
              }}
            />
          </Source>
        )}

        {popupInfo && (
          <Popup
            longitude={popupInfo.longitude}
            latitude={popupInfo.latitude}
            anchor="bottom"
            onClose={() => setPopupInfo(null)}
            closeButton={true}
            closeOnClick={false}
          >
            <div className="popup-content">
              <h3>{popupInfo.country_name}</h3>
              <div className="popup-details">
                <div className="popup-row">
                  <span>Score:</span>
                  <strong>{popupInfo.score?.toFixed(1)}</strong>
                </div>
                <div className="popup-row">
                  <span>Rank:</span>
                  <strong>#{popupInfo.global_rank}</strong>
                </div>
                <div className="popup-row">
                  <span>Status:</span>
                  <span className={`classification ${popupInfo.classification?.toLowerCase().replace(' ', '-')}`}>
                    {popupInfo.classification}
                  </span>
                </div>
              </div>
              <button
                className="popup-button"
                onClick={handleCountrySelect}
              >
                View Details →
              </button>
            </div>
          </Popup>
        )}
      </Map>

      <div className="map-legend">
        <h4>Classification</h4>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#2E7D32' }}></span>
          <span>Strongly Improving</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#66BB6A' }}></span>
          <span>Improving</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#FDD835' }}></span>
          <span>Neutral</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#FB8C00' }}></span>
          <span>Deteriorating</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: '#D32F2F' }}></span>
          <span>Strongly Deteriorating</span>
        </div>
      </div>
    </div>
  );
}

export default MomentumMap;
