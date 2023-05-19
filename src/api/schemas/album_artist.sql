create table
  public.album_artist (
    album_artist_id bigint generated by default as identity not null,
    album_id bigint null,
    artist_id bigint null,
    constraint album_artist_pkey primary key (album_artist_id),
    constraint album_artist_album_id_fkey foreign key (album_id) references albums (album_id),
    constraint album_artist_artist_id_fkey foreign key (artist_id) references artists (artist_id)
  ) tablespace pg_default;