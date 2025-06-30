const MoodSongsSection = ({ songs, mood }) => {
  if (!mood || songs.length === 0) return null;

  return (
    <section className="mood-songs">
      <h2>{mood.name} Songs</h2>
      <ul>
        {songs.map(song => (
          <li key={song.id}>
            <img src={song.image_url} alt={song.title} width={50} />
            {song.title}
          </li>
        ))}
      </ul>
    </section>
  );
};

export default MoodSongsSection;
