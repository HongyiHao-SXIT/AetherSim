#include <bits/stdc++.h>
#include <filesystem>
namespace fs = std::filesystem;

typedef unsigned int uint32;
typedef unsigned long long uint64;

std::string sha1_hex(const std::string &s);

std::string to_hex(const unsigned char* data, size_t len){
    static const char* hex = "0123456789abcdef";
    std::string out; out.reserve(len*2);
    for(size_t i=0;i<len;i++){
        unsigned char c = data[i];
        out.push_back(hex[c>>4]);
        out.push_back(hex[c&0xF]);
    }
    return out;
}

// A small SHA1 implementation (adapted)
class SHA1 {
public:
    SHA1(){ reset(); }
    void update(const unsigned char* data, size_t len){
        while(len--){
            uint8_t c = *data++;
            m_data[m_blockByteIndex++] = c;
            m_byteCount++;
            if(m_blockByteIndex == 64){
                processBlock();
                m_blockByteIndex = 0;
            }
        }
    }
    void final(unsigned char hash[20]){
        // padding
        m_data[m_blockByteIndex++] = 0x80;
        if(m_blockByteIndex > 56){
            while(m_blockByteIndex < 64) m_data[m_blockByteIndex++] = 0;
            processBlock();
            m_blockByteIndex = 0;
        }
        while(m_blockByteIndex < 56) m_data[m_blockByteIndex++] = 0;
        uint64 bitCount = m_byteCount * 8;
        for(int i=7;i>=0;i--){
            m_data[m_blockByteIndex++] = (bitCount >> (i*8)) & 0xFF;
        }
        processBlock();
        for(int i=0;i<5;i++){
            hash[i*4+0] = (m_h[i] >> 24) & 0xFF;
            hash[i*4+1] = (m_h[i] >> 16) & 0xFF;
            hash[i*4+2] = (m_h[i] >> 8) & 0xFF;
            hash[i*4+3] = (m_h[i] >> 0) & 0xFF;
        }
    }
private:
    void reset(){
        m_h[0]=0x67452301; m_h[1]=0xEFCDAB89; m_h[2]=0x98BADCFE;
        m_h[3]=0x10325476; m_h[4]=0xC3D2E1F0;
        m_blockByteIndex = 0;
        m_byteCount = 0;
    }
    void processBlock(){
        uint32 w[80];
        for(int i=0;i<16;i++){
            w[i] = ((uint32)m_data[i*4+0] << 24) |
                   ((uint32)m_data[i*4+1] << 16) |
                   ((uint32)m_data[i*4+2] << 8) |
                   ((uint32)m_data[i*4+3] << 0);
        }
        for(int i=16;i<80;i++){
            uint32 v = w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16];
            w[i] = (v << 1) | (v >> 31);
        }
        uint32 a = m_h[0], b = m_h[1], c = m_h[2], d = m_h[3], e = m_h[4];
        for(int i=0;i<80;i++){
            uint32 f, k;
            if(i<20){ f = (b & c) | ((~b) & d); k=0x5A827999; }
            else if(i<40){ f = b ^ c ^ d; k=0x6ED9EBA1; }
            else if(i<60){ f = (b & c) | (b & d) | (c & d); k=0x8F1BBCDC; }
            else { f = b ^ c ^ d; k=0xCA62C1D6; }
            uint32 temp = ((a<<5) | (a>>27)) + f + e + k + w[i];
            e = d; d = c; c = (b<<30)|(b>>2); b = a; a = temp;
        }
        m_h[0]+=a; m_h[1]+=b; m_h[2]+=c; m_h[3]+=d; m_h[4]+=e;
    }

    uint32 m_h[5];
    unsigned char m_data[64];
    size_t m_blockByteIndex;
    uint64 m_byteCount;
};

std::string sha1_hex(const std::string &s){
    SHA1 sha;
    sha.update((const unsigned char*)s.data(), s.size());
    unsigned char digest[20];
    sha.final(digest);
    return to_hex(digest, 20);
}

/* --- mini git-like implementation --- */

const std::string REPO_DIR = ".minigit";
const std::string OBJECTS_DIR = ".minigit/objects";
const std::string HEAD_FILE = ".minigit/HEAD";
const std::string INDEX_FILE = ".minigit/index"; // very simple staging: list of blob hashes and filenames
const std::string LOG_FILE = ".minigit/log";     // simple linear log (commit hashes)

void die(const std::string &msg){ cerr << "Error: " << msg << "\n"; exit(1); }

bool repo_exists(){
    return fs::exists(REPO_DIR) && fs::is_directory(REPO_DIR);
}

void repo_init(){
    if(repo_exists()){
        cout << "Repository already exists.\n";
        return;
    }
    fs::create_directory(REPO_DIR);
    fs::create_directory(OBJECTS_DIR);
    // HEAD points to last commit hash (or empty)
    ofstream(HEAD_FILE) << "\n";
    ofstream(INDEX_FILE) << ""; // empty staging
    ofstream(LOG_FILE) << "";
    cout << "Initialized empty minigit repository in " << fs::absolute(REPO_DIR) << "\n";
}

string write_object(const string &type, const string &content){
    // object format: "<type> <size>\0<content>"
    string header = type + " " + to_string(content.size()) + '\0';
    string store = header + content;
    string hash = sha1_hex(store);
    // path: objects/xx/xxxx...
    string dir = OBJECTS_DIR + "/" + hash.substr(0,2);
    string path = dir + "/" + hash.substr(2);
    if(!fs::exists(dir)) fs::create_directory(dir);
    if(!fs::exists(path)){
        ofstream ofs(path, ios::binary);
        ofs << store;
    }
    return hash;
}

bool read_object(const string &hash, string &type, string &content){
    if(hash.size() < 4) return false;
    string dir = OBJECTS_DIR + "/" + hash.substr(0,2);
    string path = dir + "/" + hash.substr(2);
    if(!fs::exists(path)) return false;
    ifstream ifs(path, ios::binary);
    string store((istreambuf_iterator<char>(ifs)), istreambuf_iterator<char>());
    // parse header
    auto pos = store.find('\0');
    if(pos==string::npos) return false;
    string header = store.substr(0,pos);
    auto sp = header.find(' ');
    if(sp==string::npos) return false;
    type = header.substr(0,sp);
    // size string omitted checking
    content = store.substr(pos+1);
    return true;
}

void add_file(const string &filename){
    if(!fs::exists(filename)) die("file does not exist: " + filename);
    if(fs::is_directory(filename)) die("can't add directory (not supported): " + filename);
    ifstream ifs(filename, ios::binary);
    string content((istreambuf_iterator<char>(ifs)), istreambuf_iterator<char>());
    string blob_hash = write_object("blob", content);
    // add to index: append "hash filename\n"
    ofstream ofs(INDEX_FILE, ios::app);
    ofs << blob_hash << " " << filename << "\n";
    cout << "Added " << filename << " (blob " << blob_hash << ")\n";
}

vector<pair<string,string>> read_index(){
    vector<pair<string,string>> res;
    if(!fs::exists(INDEX_FILE)) return res;
    ifstream ifs(INDEX_FILE);
    string line;
    while(getline(ifs,line)){
        if(line.empty()) continue;
        stringstream ss(line);
        string h,f;
        ss >> h;
        getline(ss, f);
        if(!f.empty() && f[0]==' ') f = f.substr(1);
        res.push_back({h,f});
    }
    return res;
}

string build_tree_hash_from_index_and_write_blob(){
    // Simplified: create a representation that lists filename and blob-hash,
    // then write a single "tree" blob with that listing.
    auto idx = read_index();
    sort(idx.begin(), idx.end(), [](auto &a, auto &b){ return a.second < b.second; });
    stringstream tree;
    for(auto &p: idx){
        tree << p.first << " " << p.second << "\n";
    }
    string tree_content = tree.str();
    string tree_hash = write_object("tree", tree_content);
    return tree_hash;
}

string get_head_commit(){
    if(!fs::exists(HEAD_FILE)) return "";
    ifstream ifs(HEAD_FILE);
    string h;
    ifs >> h;
    return h;
}

void update_head(const string &commit_hash){
    ofstream ofs(HEAD_FILE);
    ofs << commit_hash << "\n";
    // append to linear log
    ofstream lof(LOG_FILE, ios::app);
    lof << commit_hash << "\n";
}

string create_commit(const string &tree_hash, const string &message){
    string parent = get_head_commit();
    stringstream ss;
    ss << "tree " << tree_hash << "\n";
    if(!parent.empty()) ss << "parent " << parent << "\n";
    ss << "author mini <mini@example.com> " << time(nullptr) << "\n\n";
    ss << message << "\n";
    string commit_hash = write_object("commit", ss.str());
    update_head(commit_hash);
    // clear index (simple behavior: clear staging after commit)
    ofstream ofs(INDEX_FILE, ios::trunc);
    ofs << "";
    cout << "Committed: " << commit_hash << "\n";
    return commit_hash;
}

void cmd_log(){
    string commit = get_head_commit();
    if(commit.empty()){ cout << "No commits yet.\n"; return; }
    // traverse following parent links
    while(!commit.empty()){
        string type, content;
        if(!read_object(commit, type, content)) break;
        cout << "commit " << commit << "\n";
        // get message: content after double newline
        auto pos = content.find("\n\n");
        string header = (pos==string::npos) ? content : content.substr(0,pos);
        string message = (pos==string::npos) ? "" : content.substr(pos+2);
        // print parent if there is one in header
        string parent = "";
        {
            stringstream ss(header);
            string line;
            while(getline(ss,line)){
                if(line.rfind("parent ",0)==0) parent = line.substr(7);
            }
        }
        cout << message << "\n\n";
        if(parent.empty()) break;
        commit = parent;
    }
}

void cmd_status(){
    auto idx = read_index();
    if(idx.empty()){ cout << "No files staged.\n"; return; }
    cout << "Staged files:\n";
    for(auto &p: idx){
        cout << "  " << p.second << " (" << p.first << ")\n";
    }
}

void cmd_cat_object(const string &hash){
    string type, content;
    if(!read_object(hash, type, content)) die("object not found: " + hash);
    cout << "type: " << type << "\n";
    cout << "----\n";
    cout << content << "\n";
}

void print_help(){
    cout << "minigit - minimal Git-like tool\n\n";
    cout << "Usage:\n";
    cout << "  minigit init                    Initialize repository\n";
    cout << "  minigit add <file>              Add file to staging\n";
    cout << "  minigit commit -m \"message\"    Commit staged files\n";
    cout << "  minigit status                  Show staging status\n";
    cout << "  minigit log                     Show commit log\n";
    cout << "  minigit cat-object <hash>       Show object content\n";
    cout << "  minigit help                    Show this help\n";
}

int main(int argc, char** argv){
    if(argc < 2){ print_help(); return 0; }
    string cmd = argv[1];
    try{
        if(cmd == "init"){
            repo_init();
        } else if(cmd == "add"){
            if(argc < 3) die("add needs a filename");
            if(!repo_exists()) die("not a minigit repository (run 'minigit init')");
            add_file(argv[2]);
        } else if(cmd == "commit"){
            if(!repo_exists()) die("not a minigit repository (run 'minigit init')");
            string message;
            // parse -m "message"
            for(int i=2;i<argc;i++){
                string a = argv[i];
                if(a == "-m" && i+1<argc){
                    message = argv[i+1];
                    break;
                }
            }
            if(message.empty()) die("commit needs -m \"message\"");
            string tree_hash = build_tree_hash_from_index_and_write_blob();
            create_commit(tree_hash, message);
        } else if(cmd == "log"){
            if(!repo_exists()) die("not a minigit repository (run 'minigit init')");
            cmd_log();
        } else if(cmd == "status"){
            if(!repo_exists()) die("not a minigit repository (run 'minigit init')");
            cmd_status();
        } else if(cmd == "cat-object"){
            if(argc < 3) die("cat-object needs a hash");
            if(!repo_exists()) die("not a minigit repository (run 'minigit init')");
            cmd_cat_object(argv[2]);
        } else if(cmd == "help"){
            print_help();
        } else {
            cout << "Unknown command: " << cmd << "\n";
            print_help();
        }
    } catch(const exception &e){
        cerr << "Exception: " << e.what() << "\n";
        return 2;
    }
    return 0;
}
