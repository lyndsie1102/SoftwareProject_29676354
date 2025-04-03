import React, { useState } from "react";

const ImageSearch = () => {
    const [query, setQuery] = useState("");
    const [images, setImages] = useState([]);  // Initialize as an empty array instead of undefined
    const [error, setError] = useState(null);

    const handleSearch = async () => {
        try {
            // Changed from query to q to match the backend expectation
            const response = await fetch(`/search_images?q=${query}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            // The API returns results in a nested structure, so we need to extract the actual images
            if (data.results) {
                setImages(data.results.map(img => ({
                    url: img.thumbnail || img.url,
                    title: img.title || 'Untitled Image'
                })));
            } else {
                setImages([]);
            }
            setError(null);
        } catch (e) {
            console.error("Error fetching images:", e);
            setError("Error fetching images. Please try again.");
            setImages([]);  // Set as empty array on error
        }
    };

    return (
        <div>
            <h2>Image Search</h2>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for images..."
            />
            <button onClick={handleSearch}>Search</button>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "10px" }}>
                {images.length > 0 ? (
                    images.map((image, index) => (
                        <div key={index}>
                            <img src={image.url} alt={image.title} style={{ maxWidth: "100%" }} />
                            <p>{image.title}</p>
                        </div>
                    ))
                ) : (
                    <p>No images to display. Try searching for something!</p>
                )}
            </div>
        </div>
    );
};

export default ImageSearch;