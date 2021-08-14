typedef enum {
    XML_CHAR_ENCODING_ERROR=   -1, 
    XML_CHAR_ENCODING_NONE=	0, 
    XML_CHAR_ENCODING_UTF8=	1, 
    XML_CHAR_ENCODING_UTF16LE=	2, 
    XML_CHAR_ENCODING_UTF16BE=	3, 
    XML_CHAR_ENCODING_UCS4LE=	4, 
    XML_CHAR_ENCODING_UCS4BE=	5, 
    XML_CHAR_ENCODING_EBCDIC=	6, 
    XML_CHAR_ENCODING_UCS4_2143=7, 
    XML_CHAR_ENCODING_UCS4_3412=8, 
    XML_CHAR_ENCODING_UCS2=	9, 
    XML_CHAR_ENCODING_8859_1=	10,
    XML_CHAR_ENCODING_8859_2=	11,
    XML_CHAR_ENCODING_8859_3=	12,
    XML_CHAR_ENCODING_8859_4=	13,
    XML_CHAR_ENCODING_8859_5=	14,
    XML_CHAR_ENCODING_8859_6=	15,
    XML_CHAR_ENCODING_8859_7=	16,
    XML_CHAR_ENCODING_8859_8=	17,
    XML_CHAR_ENCODING_8859_9=	18,
    XML_CHAR_ENCODING_2022_JP=  19,
    XML_CHAR_ENCODING_SHIFT_JIS=20,
    XML_CHAR_ENCODING_EUC_JP=   21,
    XML_CHAR_ENCODING_ASCII=    22 
} xmlCharEncoding;

struct _xmlCharEncodingHandler {
    char                       *name;
    int   input;
    char  output[128];
};

void xmlInitCharEncodingHandlers(void);
int xmlAddEncodingAlias (const char *name, const char *alias);