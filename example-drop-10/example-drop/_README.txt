# ZORA Drops example folder

Your drop folder should contain a media folder, containing a media file for each NFT in the collection and an optional CSV file with metadata for all NFTS in the collection.

## Media

Media should be added inside the `media` folder.
Media must be numbered in a sequence starting from 1. ie. `1.png`, `2.png`, `3.jpg`, etc. These numbers will align with the NFT collection Token ID number and will be minted in this order. File types supported include mp3, mp4, jpg, gif, png and svg.

 If you are using non-image media (audio/video), then you can also use the thumbnail folder to upload images for marketplaces to display on list pages. By default they will match on filename `media/1.mp3 -> thumbnails/1.png`

## CSV (optional)

If you omit the CSV file the NFTs will get standard names and descriptions inherited from the collection details (set during the creation flow on <https://create.zora.co/create/drop>). Until you have entered the collection name / description on step 3, these will hold the placeholder text {collection_name} and {collection_description}.

By default, the first image `1.png` will map to the first data row of the CSV, the second image `2.png` will map to the second row and so on.

The CSV file supports adding a column named `media`, which can be used to either manually link files to metadata by using filenames, ie. `image-001.png`, or alternatively you can use https or ipfs urls here instead. It also supports a `thumbnail` column, so you can attach images to non-image media.

To set attributes on your tokens, you can use column headers prefixed with `attributes[]`, ie. `attributes[Hair color]`, `attributes[Background]`, etc.
