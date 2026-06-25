from recommendation_engine.candidate_filter import filter_candidates

movie_name = input("Enter movie name: ")

candidates = filter_candidates(movie_name)

if candidates is None:
    print("Movie not found.")
else:
    print(f"\nCandidates found: {len(candidates)}\n")
    print(candidates[["title", "genres", "original_language"]].head(10))