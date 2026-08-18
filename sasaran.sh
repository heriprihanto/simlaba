#!/bin/bash

URL="https://sipd-ri.kemendagri.go.id/rpjpd/0c1b47617452f9b2677bfe80be1b0197951afd06/"

IDSASARAN=(
    "1d30720a-40ea-11f0-aabc-622aabdf4862"
"2ecd6888-40ea-11f0-aabc-622aabdf4862"
"35d0891a-91d2-11f0-ab0c-622aabdf4862"
"3f539dda-40ea-11f0-aabc-622aabdf4862"
"53a49730-40ea-11f0-aabc-622aabdf4862"
"62fcd810-40e9-11f0-aabc-622aabdf4862"
"63625590-40ea-11f0-aabc-622aabdf4862"
"7004e112-91d2-11f0-ab0c-622aabdf4862"
"77b13800-40e9-11f0-aabc-622aabdf4862"
"7859607e-40ea-11f0-aabc-622aabdf4862"
"843cbde6-40ea-11f0-aabc-622aabdf4862"
"884dd684-91d2-11f0-ab0c-622aabdf4862"
"8dbf72b0-40e9-11f0-aabc-622aabdf4862"
"954bc9f4-91d2-11f0-ab0c-622aabdf4862"
"96987502-40ea-11f0-aabc-622aabdf4862"
"a8047a7a-40ea-11f0-aabc-622aabdf4862"
"aa9c1214-91d1-11f0-ab0c-622aabdf4862"
"b12a3152-91d1-11f0-ab0c-622aabdf4862"
"bbfbbdcc-40ea-11f0-aabc-622aabdf4862"
"bdc11536-40e9-11f0-aabc-622aabdf4862"
"c338f9b6-8f6d-11f0-ab0a-622aabdf4862"
"d08101a8-40ea-11f0-aabc-622aabdf4862"
"d9d01c80-40ea-11f0-aabc-622aabdf4862"
"e5ee12ba-40ea-11f0-aabc-622aabdf4862"
)

COOKIE_PEMDA='{"domain":"tegal.sipd.kemendagri.go.id","nama":"KOTA TEGAL"}'
PHPSESSID="4n2gj2lvl5au6qg8svnm25lq63"

TMP_FILE=$(mktemp)

# Awal array JSON
echo '[]' > "$TMP_FILE"

for ID in "${IDSASARAN[@]}"; do
    echo "Request idsasaran: $ID"

    RESPONSE=$(curl -sS \
        "$URL?m=daerah_rpjmd_d_final_sasaran&f=datatable_indikator_sasaran" \
        -H 'accept: application/json, text/javascript, */*; q=0.01' \
        -H 'accept-language: en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7' \
        -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \
        -H 'origin: https://sipd-ri.kemendagri.go.id' \
        -H 'referer: https://sipd-ri.kemendagri.go.id/' \
        -H 'x-requested-with: XMLHttpRequest' \
        -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/148.0.0.0 Safari/537.36' \
        -b "pemda=$(printf '%s' "$COOKIE_PEMDA" | jq -sRr @uri); PHPSESSID=$PHPSESSID" \
        --data-urlencode "draw=1" \
        --data-urlencode "idsasaran=$ID"
    )

    # Cek apakah response valid JSON
    if ! echo "$RESPONSE" | jq empty >/dev/null 2>&1; then
        echo "ERROR: Response bukan JSON untuk $ID"
        continue
    fi

    # Gabungkan data ke array utama
    jq -s '.[0] + (.[1].data // [])' \
        "$TMP_FILE" <(echo "$RESPONSE") > "${TMP_FILE}.new"

    mv "${TMP_FILE}.new" "$TMP_FILE"
done

mv "$TMP_FILE" indikator_sasaran.json

echo "Selesai."
echo "Total data: $(jq length indikator_sasaran.json)"