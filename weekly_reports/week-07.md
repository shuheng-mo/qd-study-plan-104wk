## 104周转行Quant | W07 - C++ IO与异常（上）

> Carol正式接任SigmaX的CTO,却发现公司的数据管理系统千疮百孔。监管审计、投资人尽调、数据丢失危机接踵而至,新官上任的Carol能否用硬核技术力挽狂澜?
> 本期关键词：IO、std::filesystem、std::format、二进制序列化、stringstream、流状态管理

## ❤️‍🔥新官上任三把火

上周SigmaX的CEO黑犬在公司完成现代化工程改造后决定退位让贤，把QD组的Leader任命为公司的新CTO。

周一一大早，Carol正式接任CTO,而Bob也从普通QD升职为了整个组的Lead。黑犬在SigmaX全员大会上宣布这一任命。富婆Esme作为主要投资人也出席了会议,她对Carol寄予厚望：

> "Carol,你的技术能力我们都看到了。现在SigmaX大大小小一共拿到了20亿融资,我们要做的第一件事就是**规范化运营**。监管部门要求我们提供**完整的数据审计追踪**,之前资金量小的时候小打小闹也就罢了，现在必须做好，这是合规的底线。"

黑犬真是脸都绿了🤢,要知道SigmaX的技术系统在过去几年里完全没有考虑过合规性(尤其是这一块还是自己兼任CTO的时候负责的),现在要补救可不是一件容易的事，还好在这个关键的时间点把烂摊子甩出去了嘻嘻。

黑犬拍了拍Carol的肩膀说：
> "Carol,这次就靠你了！合规性搞好了，我们才能安心做投资，作为CTO的侬一定不要让我们失望哦~"

Carol信心满满地接下任务,但当她开始梳理现有系统时,发现了一个可怕的事实：

- **数据文件散落在各个目录**,没有统一管理
- **日志输出全是cout/cerr**,格式混乱无法追溯
- **策略回测数据只存在内存**,重启就丢失
- **与第三方数据供应商对接靠手工复制粘贴CSV**
- **文件IO错误处理基本为零**

这哪里是管理20亿资产的量化私募的系统,这简直是大学生大课作业的水平😨！

> "XX的，这个系统也太烂了吧，我就知道这货技术不行，怪不得突然就把我升成 CTO了，整半天是这XX的烂摊子搞不定了吧！"

Carol真的气炸了，决定立刻召集QD组开会，制定一套**现代C++文件和数据管理系统**的改造方案，同时在QD部门的会议室里把黑犬骂了个狗血淋头。

此时在办公室喝马黛茶🧉看彭博新闻的黑犬忽然打了一个喷嚏🤧。

## 🔍技术噩梦还是审计噩梦

周二的时候，监管部门来了一次突击检查。证监会的审计官员来到SigmaX进行季度审计,要求提供：

1. **所有策略的历史执行记录**（谁、何时、执行了什么策略）
2. **数据文件的完整性验证**（文件是否被篡改、何时创建）
3. **系统日志的时间轴**（精确到毫秒的操作记录）

审计官拿出一份文件清单："请提供2025年Q3季度所有交易策略的执行日志,按日期归档。"

接到合规官Henry需求的Bob打开服务器一看,傻眼了：

```
/home/sigmaq/
├── log.txt          # 所有日志混在一起
├── data.csv         # 不知道是什么数据
├── backup/          # 空文件夹
├── temp123.dat      # 临时文件没清理
└── ...              # 一堆乱七八糟的文件
```

审计官皱起眉头："你们的文件管理怎么这么混乱?我需要看到**规范的目录结构**,每天的日志应该独立存放,历史数据要有备份机制。"

Carol也被问得非常无语,她只能硬着头皮说：
> "非常抱歉,我们之前没有重视这方面的管理,现在请给我3天时间。我会用C++17的**std::filesystem**重构整个数据管理系统,建立规范的目录结构和自动备份机制。"

结合周一开会的规划，Carol连夜召集Bob和Alice,开始构建公司数据管理功能**DataManager**：

```cpp
// 代码文件：code/week-07/DataManager.hpp
// 建立规范的目录结构
./quant_data/
  ├── data/
  │   ├── strategies/      # 策略数据
  │   ├── portfolios/      # 组合数据
  │   └── market_data/     # 行情数据
  ├── backup/              # 自动备份
  │   ├── daily/
  │   └── weekly/
  └── logs/                # 日志文件
      ├── 2024-12-01.log
      ├── 2024-12-02.log
      └── ...
```

在构建DataManager时，Carol使用了std::filesystem的强大功能来实现文件和目录的创建、删除、遍历等操作，核心功能包括：

- **自动创建目录结构** (fs::create_directories)
- **文件存在性检查** (fs::exists)
- **自动备份机制** (fs::copy_file)
- **清理过期文件** (fs::last_write_time)
- **目录大小统计** (fs::file_size)

3天后,审计官再次来访,Carol演示了新系统：

> "您看,这是我们的策略执行目录。每个策略都有独立的数据文件,自动按日期归档。系统会自动备份重要数据,并清理30天前的临时文件。所有文件操作都有完整的元数据记录。"

审计官满意地点头："这才像一个专业的金融机构！通过！"

## 👠富婆的话你要听

周三上午在投资人例会上，Esme带着几位新的LP来到SigmaX,并提出新的透明化运营的要求：

> "狗子,我们这帮人投了这么多钱,需要实时了解系统运行状态。我要求所有关键操作都要有**格式化日志**,包括：
>
> - 谁在什么时间执行了什么操作
> - 每个策略的收益率,精确到小数点后4位
> - 系统性能指标,响应时间要精确到毫秒
>
> 而且日志要**易读、专业、可追溯**,不要再给我看那些cout输出的垃圾！"

黑犬听得冷汗直流，但是有不能不答应投资人的要求，只有先在会上打哈哈说官话，然后不时给Carol使眼色，整的Carol坐在对面很无语，白眼都要翻到天上了🫣。

Bob私下对Carol说："老板,现在的日志系统全是老板那XX硬编码的cout,要改成格式化输出得重写几千行代码,还容易出错😵..."

Carol想起了C++20的**std::format**：

> "不用重写！我们用std::format构建统一的**Logger系统**。类型安全、高性能、Python风格的格式化语法,完美契合我们的需求！"

Carol设计了分级日志系统：

```cpp
// 代码文件：code/week-07/Logger.hpp
// 日志级别：DEBUG < INFO < WARNING < ERROR

// 使用示例
logger.info("Team {} hired {} new members", "SigmaX-QD", 5);
// 输出: [2024-12-26 14:32:15] [INFO] Team SigmaX-QD hired 5 new members

logger.warning("Portfolio drawdown: {:.2f}%", -15.3);
// 输出: [2024-12-26 14:35:20] [WARNING] Portfolio drawdown: -15.30%

logger.error("Strategy {} failed: {}", "MomentumV2", "Insufficient data");
// 输出: [2024-12-26 14:40:01] [ERROR] Strategy MomentumV2 failed: Insufficient data
```

在新的日志系统中，实现了以下核心特性：

- **类型安全的格式化**（编译期检查,杜绝printf的类型错误）
- **自动时间戳**（精确到秒,支持自定义格式）
- **分级日志**（DEBUG/INFO/WARNING/ERROR）
- **同时输出到文件和控制台**
- **高性能**（比iostream快,比printf安全）

在此基础上，为了堵住所有投资人的嘴，Carol还设计了投资报告生成器功能，一键生成每日投资数据报告：

```cpp
// 代码文件：code/week-07/ReportGenerator.hpp
╔══════════════════════════════════════╗
║  Portfolio Report: Alpha-Fund        ║
╚══════════════════════════════════════╝

Symbol      Quantity          Price          Value
------------------------------------------------------------
AAPL             500      $  175.25  $   87,625.00
TSLA             300      $  248.50  $   74,550.00
NVDA             200      $  495.75  $   99,150.00
------------------------------------------------------------
TOTAL                                  $  261,325.00
============================================================
```

Esme看到投资报告后赞不绝口："这才是专业机构该有的水准！比我投的其他基金都专业！狗子你这Carol能力太强了，她结婚了么？你和她说说要不要我给介绍个好对象哈哈哈~"

黑犬笑而不语🤩，给她介绍对象？算了吧，这么好用的CTO最好就一直别结婚为我所用，这份工资发的太值了😈。

## 🤪策略(又又)要爆了

周四凌晨两点，Alice慌张地给Carol打了一通紧急电话：
> "Carol！出大事了！服务器刚才重启,我的**动量突破策略V3**的回测数据**全部丢失**！那可是我调了3个月的参数啊😭！年化收益率48%的策略,现在什么都没了！"

Carol远程登录服务器一查,心都凉了：所有策略数据都只存在内存里,从来没有持久化过！最糟糕的时，这次的问题还赖不上黑犬，完全是之前跳槽的QD成员遗留下来的问题。

黑犬半夜在公司飞书群里发飙：
> @全体成员 明天早上投资委员会要审查所有策略的历史回测数据,这要是拿不出东西来,Esme朋友给的2亿融资可能要黄！Carol,必须在8小时内搞出点东西来拿给委员会看！不然就收拾东西滚蛋吧！

Carol知道数据已经无法恢复,但她可以立即建立**持久化系统**,防止悲剧再次发生。她决定用**二进制序列化**：

```cpp
// 代码文件：code/week-07/Serialization.hpp
// 二进制序列化系统

// 保存策略数据
struct StrategyData {
    std::string name;
    double annual_return;
    double sharpe_ratio;
    std::vector<double> daily_returns;

    void serialize(BinarySerializer& ser) const;
    static StrategyData deserialize(BinaryDeserializer& deser);
};

// 使用
StrategyData strategy{"MomentumV3", 0.48, 2.1, {...}};
TeamPersistence::save_strategy("momentum_v3.bin", strategy);

// 下次直接加载,数据永不丢失！
auto loaded = TeamPersistence::load_strategy("momentum_v3.bin");
```

早上8点,Carol向投资委员会演示：

> "各位,虽然历史数据丢失了,但我已经建立了完善的持久化系统。从今天起,所有策略的回测数据都会自动保存为二进制文件,即使服务器重启,数据也永不丢失。"

投资委员会成员问："为什么用二进制而不是JSON?"

Carol自信地回答：
> "二进制序列化的读写速度是JSON的**10倍以上**,文件大小只有JSON的**30%**。对于我们每天产生GB级别的回测数据来说,这是性能和存储空间的最优解。而且我们实现了版本控制,未来升级数据格式也不会破坏兼容性。"

投资人们纷纷点头,这次虽然没有完美解决问题，但是好在还是给了投资人信心，危机化解，黑犬也没有再给技术部门施压，只是叮嘱各位以后要听Carol的话，不要再出幺蛾子了。

## 💩头铁的乙方

SigmaX签约了彭博(Bloomberg)的市场数据服务,对方技术负责人David说：

> "我们的数据接口支持CSV格式导出,你们需要每天早上9点从我们的FTP服务器拉取最新的市场数据CSV文件,然后导入你们的系统。"

Bob一听就头大："CSV格式?那不是要写一堆字符串解析代码?万一数据里有逗号、换行符这些特殊字符怎么办?"

Carol说："不用担心,我们用**std::stringstream**来优雅地处理CSV导入导出！"

```cpp
// 代码文件：code/week-07/CSVHandler.hpp
// CSV导出
std::string csv = CSVExporter::export_portfolio_csv(portfolio);
// 输出:
// Symbol,Quantity,Price,Value
// AAPL,500,175.25,87625.00
// TSLA,300,248.50,74550.00

// CSV导入
auto portfolio = CSVImporter::import_portfolio_csv(csv_data);
```

实现了几个核心特性：

- **内存中的流操作**（不需要临时文件）
- **灵活的格式控制**（setprecision控制精度）
- **字符串拆分解析**（getline配合delimiter）
- **类型转换**（string → double/int）

David看了Carol的实现后说："你们的CSV处理很专业！很多量化公司都是用Python脚本手工处理,你们直接在C++里实现,性能肯定好得多。"

第二天早上,系统成功从彭博拉取了最新数据,自动解析导入,整个流程不到10秒完成。

## 🚨突发情况

正当Carol以为一切顺利时,周六的上午交易系统突然报错：

```
Error: Failed to write trade log
Error: Cannot open portfolio file
Error: Data file corrupted
```

Carol紧急排查,发现问题出在**IO错误处理**上：

- **磁盘空间不足**,写入失败但没有检测
- **文件权限错误**,打开文件失败被忽略
- **网络文件系统断线**,读取数据时出错但没有异常处理

这些错误在测试环境都没暴露,一到生产环境就频繁出现,导致交易系统数据不一致😱！

Carol痛定思痛,决定实现**完善的流状态管理**：

```cpp
// 代码文件：code/week-07/SafeFileIO.hpp
class SafeFileReader {
public:
    static std::string read_file(const fs::path& path) {
        std::ifstream ifs(path);

        // 检查打开状态
        if (!ifs.is_open()) {
            throw std::runtime_error(
                std::format("Cannot open file: {}", path.string())
            );
        }

        // 启用异常
        ifs.exceptions(std::ifstream::badbit);

        // 检查读取状态
        if (ifs.bad()) {
            throw std::runtime_error("Error reading file");
        }

        return content;
    }
};
```

实现了以下核心特性：

- **is_open()** 检查文件是否成功打开
- **exceptions()** 启用流异常
- **good()/bad()/fail()/eof()** 状态检查
- **详细的错误信息** (std::format)

重构后,系统运行稳定,再也没有出现过IO相关的生产事故。

## 🪞Carol的周末复盘

周日晚上，Carol在家坐在电脑前复盘整理这一周的技术总结报告，一周的奋战让她又掉了几根头发😵‍💫，但看到新闻报道SigmaX的技术领先行业还是有了几分欣慰。

黑犬发来微信："Carol,这周辛苦了。你的技术改造让投资人和监管部门都非常满意,明天我会给你和QD组发一笔特别奖金💰。继续加油,SigmaX的未来就靠你们了！"

Carol苦笑,回复："放心吧老板,下周我们会把异常处理也做到业界顶尖水平！"

经过一周的血与泪,SigmaX的数据管理系统已经脱胎换骨,Carol也成功化解了多重危机。她知道,作为CTO,未来的挑战只会更多,不管这些挑战是来自内部还是外部,她都将带领QD组迎难而上,用硬核技术守护SigmaX的每一分资产和尊严。

## 📒补充说明

本周学习的5个核心IO技术,都是现代C++的最佳实践：

1. std::filesystem (C++17)
2. std::format (C++20)
3. 二进制序列化
4. std::stringstream
5. 流状态管理

这些模式的共同点是：**在运行时保持灵活性的同时，尽可能利用编译期优化**。至此我们已经在SigmaX完成了所有最常见的C++ 现代化技术中文件IO的所有实践，下周开始，我们将进入C++基础的又一大话题：异常。

你可能要问，IO不还有网络IO吗？没有错，但是网络IO的内容实在太多涉及的场景也更加复杂，需要搭建专门的网络环境来解释和，我们会在后续设置一个单独的专题展开讲解，欢迎关注，敬请期待~

本周代码已经上传到Github仓库🔗：[https://github.com/shuheng-mo/qd-study-plan-104wk.git](https://github.com/shuheng-mo/qd-study-plan-104wk.git)，欢迎Star⭐、贡献代码或issue。

**下周预告：W08 - C++ IO与异常(下)**

👋各位下周五见，下周SigmaX又会有哪些有趣的故和硬核挑战呢？尽情期待吧~
