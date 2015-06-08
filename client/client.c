#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <netdb.h>
#include <netinet/in.h>
#include <string.h>
#include <stdlib.h>
#include <getopt.h>

char *my_sdp = "v=0 \n\
        o=- 3414953978 3414953978 IN IP4 localhost \n\
        s=ice \n\
        t=0 0 \n\
        a=ice-ufrag:518f5329 \n\
        a=ice-pwd:78f2ca8e \n\
        m=audio 56873 RTP/AVP 0 \n\
        c=IN IP4 10.0.0.102 \n\
        a=candidate:Sa000066 1 UDP 1862270975 14.161.16.36 56873 typ srflx \n\
        a=candidate:Ha000066 1 UDP 1694498815 10.0.0.102 56873 typ host \n";


char id[256];

char host_name[256];
int portno;


void help()
{
    printf("cmd list: \n \t g id: get dsp of an id \n");
    printf("\t a: get all id \n");
    printf("\t p: put dsp\n");

}

static void hexDump (char *desc, void *addr, int len) {
    int i;
    unsigned char buff[17];
    unsigned char *pc = (unsigned char*)addr;

    // Output description if given.
    if (desc != NULL)
        printf ("%s:\n", desc);

    // Process every byte in the data.
    for (i = 0; i < len; i++) {
        // Multiple of 16 means new line (with line offset).

        if ((i % 16) == 0) {
            // Just don't print ASCII for the zeroth line.
            if (i != 0)
                printf ("  %s\n", buff);

            // Output the offset.
            printf ("MSGMSG  %04x ", i);
        }

        // Now the hex code for the specific character.
        printf (" %02x", pc[i]);

        // And store a printable ASCII character for later.
        if ((pc[i] < 0x20) || (pc[i] > 0x7e))
            buff[i % 16] = '.';
        else
            buff[i % 16] = pc[i];
        buff[(i % 16) + 1] = '\0';
    }

    // Pad out last line if not exactly 16 characters.
    while ((i % 16) != 0) {
        printf ("   ");
        i++;
    }

    // And print the final ASCII bit.
    printf ("  %s\n", buff);
}



static int peer_put_dsp(char *my_id, char *_dsp)
{
    int sockfd, n;
    struct sockaddr_in serv_addr;
    struct hostent *server;

    char buffer[1024];
    /* Create a socket point */
    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    if (sockfd < 0)
    {
        perror("ERROR opening socket");
        exit(1);
    }
    server = gethostbyname(host_name);

    if (server == NULL) {
        fprintf(stderr,"ERROR, no such host\n");
        exit(0);
    }

    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);
    serv_addr.sin_port = htons(portno);

    /* Now connect to the server */
    if (connect(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0)
    {
        perror("ERROR connecting");
        exit(1);
    }


    bzero(buffer,1024);
    sprintf(buffer, "PUT_%d_%s_%s\n", strlen(my_id) + strlen(_dsp) + 2, my_id, _dsp);
    //fgets(buffer,255,stdin);
    printf("[Debug] %s, %d \n", __FILE__, __LINE__);

    /* Send message to the server */
    n = write(sockfd, buffer, strlen(buffer));

    printf("[Debug] %s, %d \n", __FILE__, __LINE__);

    if (n < 0)
    {
        perror("ERROR writing to socket");
        exit(1);
    }
    printf("[Debug] %s, %d \n", __FILE__, __LINE__);

    //usleep(50*1000*1000);

    /* Now read server response */
    bzero(buffer,1024);
    n = read(sockfd, buffer, 1024);
    printf("[Debug] %s, %d \n", __FILE__, __LINE__);

    hexDump(NULL, buffer, n);


    close(sockfd);

}


int main(int argc, char *argv[])
{
    printf("my sdp: %s \n", my_sdp);
    strcpy(id, "defaultusr");

#if 0
    while (1)
    {
        static struct option long_options[] =
        {
            /* These options set a flag. */
            {"id",    required_argument, 0, 'i'},
            {0, 0, 0, 0}
        };
        /* getopt_long stores the option index here. */
        int option_index = 0;

        c = getopt_long (argc, argv, "i",
                         long_options, &option_index);

        /* Detect the end of the options. */
        if (c == -1)
            break;

        switch (c)
        {

        case 'i':
            printf ("[Debug] user id: %s\n", optarg);
            strcpy(id, optarg);
            break;

        default:
            abort ();
        }
    }

#endif
#if 0
    int sockfd, portno, n;
    struct sockaddr_in serv_addr;
    struct hostent *server;

    char buffer[1024];
#endif
    if (argc <4) {
        fprintf(stderr,"usage %s hostname port\n", argv[0]);
        exit(0);
    }

    strcpy(host_name, argv[1]);
    portno = atoi(argv[2]);
    strcpy(id, argv[3]);

#if 0
    /* Create a socket point */
    sockfd = socket(AF_INET, SOCK_STREAM, 0);

    if (sockfd < 0)
    {
        perror("ERROR opening socket");
        exit(1);
    }
    server = gethostbyname(argv[1]);

    if (server == NULL) {
        fprintf(stderr,"ERROR, no such host\n");
        exit(0);
    }

    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);
    serv_addr.sin_port = htons(portno);

    /* Now connect to the server */
    if (connect(sockfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0)
    {
        perror("ERROR connecting");
        exit(1);
    }
#endif

    char cmd;
    do {
        printf(">>> ");
        cmd = getchar();
        printf("[Debug] command character: %c \n", cmd);
        while (getchar() != '\n');

        if (cmd == 'p')
        {
            peer_put_dsp(id, my_sdp);
    #if 0
            bzero(buffer,1024);
            sprintf(buffer, "PUT_%d_%s_%s\n", strlen(id) + strlen(my_sdp) + 2, id, my_sdp);
            //fgets(buffer,255,stdin);
            printf("[Debug] %s, %d \n", __FILE__, __LINE__);

            /* Send message to the server */
            n = write(sockfd, buffer, strlen(buffer));

            printf("[Debug] %s, %d \n", __FILE__, __LINE__);

            if (n < 0)
            {
                perror("ERROR writing to socket");
                exit(1);
            }
            printf("[Debug] %s, %d \n", __FILE__, __LINE__);

            //usleep(50*1000*1000);

            /* Now read server response */
            bzero(buffer,1024);
            n = read(sockfd, buffer, 1024);
            printf("[Debug] %s, %d \n", __FILE__, __LINE__);

            hexDump(NULL, buffer, n);
#endif

        }else if (cmd == 'g')
        {
#if 0
            printf("Input the id: ");
            char _id[256];
            gets(_id);

            bzero(buffer,1024);
            sprintf(buffer, "GET_%d_%s_AAAAAA\n", strlen(id) + strlen(my_sdp) + 2, id);
            //fgets(buffer,255,stdin);

            /* Send message to the server */
            n = write(sockfd, buffer, strlen(buffer));

            if (n < 0)
            {
                perror("ERROR writing to socket");
                exit(1);
            }
            /* Now read server response */
            bzero(buffer,1024);
            n = read(sockfd, buffer, 1024);

            hexDump(NULL, buffer, n);
           #endif

        }else if (cmd == 'h')
        {
            help();
        }

    } while (cmd != 'q');



    return 0;
}
