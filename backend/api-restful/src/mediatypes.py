class MediaTypes:
    # General Text Types
    TEXT_PLAIN = "text/plain"
    TEXT_HTML = "text/html"
    TEXT_CSS = "text/css"
    TEXT_JAVASCRIPT = "text/javascript"
    TEXT_CSV = "text/csv"
    TEXT_XML = "text/xml"

    # General Application Types
    APPLICATION_JSON = "application/json"
    APPLICATION_XML = "application/xml"
    APPLICATION_JAVASCRIPT = "application/javascript"
    APPLICATION_XHTML_XML = "application/xhtml+xml"
    APPLICATION_FORM_URLENCODED = "application/x-www-form-urlencoded"
    APPLICATION_PDF = "application/pdf"
    APPLICATION_ZIP = "application/zip"
    APPLICATION_OCTET_STREAM = "application/octet-stream"

    # Multipart Types
    MULTIPART_FORM_DATA = "multipart/form-data"
    MULTIPART_ALTERNATIVE = "multipart/alternative"
    MULTIPART_MIXED = "multipart/mixed"

    # Image Types
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"
    IMAGE_GIF = "image/gif"
    IMAGE_SVG_XML = "image/svg+xml"
    IMAGE_WEBP = "image/webp"
    IMAGE_BMP = "image/bmp"

    # Audio Types
    AUDIO_MPEG = "audio/mpeg"
    AUDIO_OGG = "audio/ogg"
    AUDIO_WAV = "audio/wave"
    AUDIO_AAC = "audio/aac"

    # Video Types
    VIDEO_MP4 = "video/mp4"
    VIDEO_OGG = "video/ogg"
    VIDEO_WEBM = "video/webm"

    # Vendor Specific Types
    APPLICATION_VND_MS_EXCEL = "application/vnd.ms-excel"
    APPLICATION_VND_WORD = (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    APPLICATION_VND_EXCEL = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    APPLICATION_TAR = "application/x-tar"
    APPLICATION_GZIP = "application/gzip"

    # Wildcard
    WILDCARD_ANY = "*/*"
