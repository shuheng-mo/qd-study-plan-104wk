## 104周转行Quant | W08 - C++ 异常处理

> 一场无声崩溃导致千万级损失，SigmaX的CTO Carol再次遇到巨大挑战。从异常层次结构到零开销错误处理，从RAII到多线程异常传播，这是一场关于错误、崩溃与救赎的硬核技术战。
> 本期关键词：异常层次、std::source_location、Expected<T,E>、error_code、RAII、异常安全、exception_ptr、多线程异常传播

## 💣无声的崩溃

周一早上9:31，SigmaX的交易大厅突然陷入死寂。

所有交易员盯着屏幕，Bob冲进Carol的办公室，脸色铁青：

> "Carol！Alpha-Plus策略刚才崩了！没有任何日志，没有任何错误信息，就这么**无声地死掉了**！我们在9:30开盘的瞬间错过了一个**价值1200万的套利机会**！黑犬气疯了，把马黛茶杯都砸了，让技术团队立刻搞定这个问题！"

Carol的心一下子沉到谷底。她立刻打开监控系统，发现问题比想象的更严重：

- 程序崩溃时没有留下任何异常信息
- 日志文件里只有一行："Segmentation fault (core dumped)"
- 核心转储文件因为磁盘满了没有生成
- 投资人实时监控系统显示策略状态为"未知"

更糟糕的是，早上10点富婆Esme就要来开投资委员会，这次还带了几个新的潜在LP。如果让他们知道系统连基本的错误报告都做不到，2亿美元的新融资就要泡汤了。

Carol看着Bob："给我把崩溃前最后执行的代码调出来。"

Bob调出代码，Carol看了一眼就明白了问题所在：

```cpp
// 旧代码 - 灾难的根源
double execute_trade(const Trade& trade) {
    auto account = get_account(trade.account_id);  // 可能返回空指针
    auto price = get_market_price(trade.symbol);    // 可能失败
    return account->balance * price;                // 💥 nullptr解引用
}
```

> "XX的！这代码连基本的错误检查都没有，难怪会无声崩溃！这是谁写的代码？"

Bob压低肩膀小声说："这是...黑犬三个月前写的核心交易模块..."

Carol深吸一口气，在心里把黑犬全家问候了一遍。她看了看时间，距离投资委员会晨会还有30分钟，于是硬着头皮和黑犬说：

> "立刻启用备用策略，然后给我3天时间。我要重写整个异常处理系统，让每一个错误都**有迹可循、有据可查**！"

黑犬咬牙切齿地说（显然不知道是自己的问题🤡）："Carol，这次你必须搞定！投资委员会那边我先去应付一下，别让我再看到这种无声崩溃了！下次再出这种问题，你就等着被炒鱿鱼吧！"

## 🏗️建立异常帝国

周一下午，Carol召集QD组紧急会议，在白板上画出了异常处理的重构蓝图：

> "各位，从今天开始，SigmaX不允许任何**静默失败**！我要建立一套完整的异常层次结构，让每一个错误都能精确定位到源码的行号！"

Alice举手："Carol，我们应该用返回错误码还是抛异常？我看到系统里很多老代码用的是返回-1表示错误..."

Carol在白板上写下："异常层次结构 + std::source_location"

> "返回错误码？那是C语言时代的做法！现代C++有**异常层次**和**source_location**，我们要让每个异常都带着完整的上下文信息：哪个文件、哪一行、什么函数、什么错误！"

Carol连夜设计了SigmaX的异常帝国版图：

```cpp
// 代码文件：code/week-08/include/Exceptions.hpp

// 基础异常类 - 所有异常的根
class QuantTeamException : public std::exception {
    std::string message;
    std::source_location location;  // 自动记录文件名、行号、函数名

    std::string get_exception_type() const {
        return "QuantTeamException";
    }
};

// 数据异常
class DataException : public QuantTeamException {};
    class FileNotFoundException : public DataException {};
    class SerializationException : public DataException {};

// 业务异常
class BusinessException : public QuantTeamException {};
    class InsufficientFundsException : public BusinessException {};
    class InvalidTradeException : public BusinessException {};
    class StrategyExecutionException : public BusinessException {};

// 系统异常
class SystemException : public QuantTeamException {};
    class NetworkException : public SystemException {};
    class ConfigurationException : public SystemException {};
```

第二天一早，Bob拿着重构后的代码演示：

```cpp
// 新代码 - 精确定位问题
double execute_trade(const Trade& trade) {
    auto account = get_account(trade.account_id);
    if (!account) {
        throw InvalidEmployeeException(
            std::format("Account {} not found", trade.account_id)
        );  // std::source_location::current() 自动捕获位置
    }

    auto price = get_market_price(trade.symbol);
    if (!price) {
        throw NetworkException(
            std::format("Failed to fetch price for {}", trade.symbol)
        );
    }

    if (account->balance < price * trade.quantity) {
        throw InsufficientFundsException(
            std::format("Account {} has insufficient funds: {} < {}",
                       trade.account_id, account->balance, price * trade.quantity)
        );
    }

    return execute_order(account, trade, *price);
}
```

当天下午测试新系统时，Alice故意触发了一个错误。日志输出：

```
[ExceptionUtils.hpp:247:32] InvalidTradeException: Invalid trade quantity: -100
  at execute_trade (Trading.cpp:156)
  called from process_order (OrderManager.cpp:89)
  called from main (main.cpp:42)
```

Carol满意地点头："这才是专业交易系统该有的样子！现在任何错误都能追溯到源头，再也不会有**无声的崩溃**了！"

## ⚡高频交易的性能焦虑

周三上午，负责高频交易的资深Quant Eric找到Carol，一脸焦虑：

> "Carol，你的异常系统很完善，但是我们的**高频做市策略**每秒要处理10万笔订单，抛异常的性能开销我们承受不起！一个异常的开销相当于几千次函数调用，这会让我们的延迟从**微秒级涨到毫秒级**，在高频领域这就是灾难！"

Carol皱眉，这确实是个问题。C++异常的性能开销主要来自栈展开（stack unwinding）和异常对象的构造，在高频场景下确实不合适。

> "你说得对。高频交易路径上不能用异常，我们需要**零开销的错误处理**。"

Carol想起了Rust的`Result<T, E>`类型和C++23的`std::expected`。虽然SigmaX还在用C++20，但她可以自己实现一个简化版！

```cpp
// 代码文件：code/week-08/include/Expected.hpp

template<typename T, typename E>
class Expected {
    std::variant<T, E> data;  // 要么是值，要么是错误

public:
    bool has_value() const;
    T& value();          // 有值则返回，否则抛异常
    E& error();          // 有错误则返回
    T value_or(T default_value);  // 有值返回值，否则返回默认值

    // 函数式操作
    auto and_then(Func func);   // 链式调用
    auto or_else(Func func);    // 错误处理
    auto transform(Func func);  // 值转换
};
```

Carol给Eric演示新的高频交易代码：

```cpp
// 高频路径 - 零开销错误处理
Expected<Price, PriceError> get_best_price(const Symbol& symbol) {
    if (auto price = market_data.find(symbol); price != market_data.end()) {
        return Expected<Price, PriceError>(price->second);
    }
    return make_unexpected(PriceError::SYMBOL_NOT_FOUND);
}

// 链式调用，优雅处理错误
auto result = get_best_price("AAPL")
    .and_then([](Price p) { return calculate_spread(p); })
    .and_then([](Spread s) { return execute_market_making(s); })
    .or_else([](auto error) {
        // 错误处理，不影响主流程
        logger.warning("Market making failed: {}", error);
    });
```

Eric跑了性能测试，兴奋地报告："Carol！新方案的延迟只有**0.3微秒**，比异常快了1000倍！而且代码还更清晰了！"

同时，为了处理一些系统级错误，Carol还引入了`std::error_code`机制：

```cpp
// 代码文件：code/week-08/include/ErrorCode.hpp

enum class QuantTeamError {
    SUCCESS = 0,
    INVALID_EMPLOYEE_ID = 1,
    DUPLICATE_EMPLOYEE = 2,
    INSUFFICIENT_FUNDS = 3,
    NETWORK_ERROR = 7,
    AUTHENTICATION_FAILED = 8,
};

// 与标准库错误系统集成
std::error_code make_error_code(QuantTeamError e) {
    return {static_cast<int>(e), quant_team_category()};
}
```

Carol解释："错误码系统适合系统级错误，`Expected`适合业务逻辑，异常适合真正的异常情况。**分层处理，各司其职**！"

## 🔄数据一致性的噩梦

周四凌晨3点，Carol又一次被电话吵醒。Bob在电话里语无伦次：

> "Carol！出大事了！组合管理系统在更新时崩溃，现在数据库里的数据**乱套了**！某个账户的持仓数据一半是新的一半是旧的，账目对不上了！合规官Henry说如果明早9点前解决不了，监管部门会介入调查！"

Carol一个激灵坐起来，这是**数据一致性问题**。系统在更新多个相关数据时，中途出错导致部分数据已修改、部分数据还是旧的，形成了**不一致状态**。

> "XXX的！这就是典型的**异常安全问题**！我怎么能给忘了！(捂脸)我马上到公司，你先别动系统，避免更多数据损坏！"

Carol披上外套直奔公司。一路上她在脑子里设计解决方案：需要**强异常保证**（Strong Exception Guarantee）—— 要么全部成功，要么全部回滚，绝不允许中间状态！

到公司后，Carol立刻开始编码：

```cpp
// 代码文件：code/week-08/include/ExceptionSafety.hpp

// Transaction - 事务模板，强异常保证
template<typename T>
class Transaction {
    T& target;
    T backup;        // 备份原始状态
    bool committed = false;

public:
    explicit Transaction(T& obj)
        : target(obj), backup(obj) {}  // 构造时备份

    ~Transaction() {
        if (!committed) {
            target = std::move(backup);  // 析构时如果未提交则回滚
        }
    }

    void commit() { committed = true; }  // 显式提交
};
```

她重写了组合更新逻辑：

```cpp
void update_portfolio(Portfolio& portfolio, const std::vector<Trade>& trades) {
    Transaction transaction(portfolio);  // 开始事务，自动备份

    // 执行所有更新
    for (const auto& trade : trades) {
        portfolio.add_trade(trade);  // 任何一步失败都会抛异常
        portfolio.update_balance(trade);
        portfolio.update_positions(trade);
    }

    transaction.commit();  // 全部成功才提交
    // 如果中途抛异常，析构函数自动回滚！
}
```

同时，Carol还实现了`ScopeGuard`来处理资源清理：

```cpp
void process_large_file(const fs::path& file_path) {
    FILE* file = fopen(file_path.c_str(), "r");
    auto guard = make_scope_guard([file]() {
        fclose(file);  // 无论如何都会关闭文件
    });

    // 处理文件，即使抛异常也会自动关闭
    process_data(file);
    // guard 析构时自动执行 cleanup
}
```

早上8:45，Carol完成了数据修复和系统重构。当监管官员9点准时到达时，看到的是一个账目完全一致、数据完整的系统。

Henry松了一口气，私下对Carol说："SigmaX没有你真是要散啊！真的把我们老板开了都不能开你~”

Carol疲惫地笑了笑："那怎么办，谁叫公司里我技术最强呢。这就是**RAII**的威力——**资源获取即初始化，析构即清理**。C++最美的设计之一。"

## 🧵多线程的异常风暴

周五下午，策略研究员Alice正在进行策略回测，突然系统报错：

```
terminate called after throwing an instance of 'DataException'
Aborted (core dumped)
```

Alice慌了："Carol！我在8个线程里并行回测不同策略，其中一个线程抛了异常，然后整个程序就崩了！其他7个线程的计算结果全丢了！"

Carol一看就明白了问题：**C++的异常不能跨线程传播**！当子线程抛出异常而没有捕获时，程序会直接调用`std::terminate()`终止。

> "多线程异常传播，这是C++异常处理最棘手的问题之一。"

Carol设计了`AsyncTaskManager`来解决这个问题：

```cpp
// 代码文件：code/week-08/include/ExceptionPropagation.hpp

class AsyncTaskManager {
    std::vector<std::exception_ptr> exceptions;  // 存储异常指针
    std::mutex exceptions_mutex;
    std::vector<std::thread> threads;

public:
    void run_task(std::function<void()> task) {
        threads.emplace_back([this, task]() {
            try {
                task();
            } catch (...) {
                // 捕获当前异常并存储
                std::lock_guard lock(exceptions_mutex);
                exceptions.push_back(std::current_exception());
            }
        });
    }

    void wait_all() {
        for (auto& t : threads) {
            t.join();
        }
    }

    void rethrow_first_exception() {
        if (!exceptions.empty()) {
            std::rethrow_exception(exceptions.front());  // 主线程重新抛出
        }
    }
};
```

Alice用新系统重写回测代码：

```cpp
AsyncTaskManager manager;

// 在多个线程中运行策略
for (const auto& strategy : strategies) {
    manager.run_task([&strategy]() {
        backtest_strategy(strategy);  // 可能抛异常
    });
}

manager.wait_all();  // 等待所有线程

// 检查是否有异常
if (manager.has_exceptions()) {
    std::cout << "Some strategies failed:\n";
    manager.handle_all_exceptions([](const std::exception& e) {
        std::cout << "  - " << e.what() << "\n";
    });
}
```

测试时，Alice故意让3个策略失败，系统完美地收集了所有异常，其他5个策略的结果都保留了下来。

> "太棒了Carol！现在即使部分策略失败，我也能看到完整的错误报告，其他策略的结果也不会丢失！"

## 🎭嵌套异常的侦探游戏

就在Carol以为可以松口气时，黑犬向公司全员转发了一封来自某个外部数据供应商的邮件：

> "SigmaX技术团队，你们今早的API调用出现了大量错误。请提供完整的错误调用栈，否则我们无法定位问题。"

Bob查看日志，发现错误信息只有一行：

```
Error: Failed to fetch market data
```

黑犬发火了："就这？这叫完整的错误信息？底层到底发生了什么？是网络超时？认证失败？还是数据格式错误？数据供应商要的是**完整的调用链**！Carol马上让技术团队搞定这个问题！"

Carol意识到问题所在：异常在传播过程中，底层的错误信息被上层异常覆盖了。她需要**嵌套异常**（Nested Exception）！

```cpp
// 底层函数
void fetch_data_from_api(const std::string& endpoint) {
    if (!network_available()) {
        throw NetworkException("Network unavailable");
    }
    // ...
}

// 中层函数 - 包装底层异常
MarketData get_market_data(const Symbol& symbol) {
    try {
        return fetch_data_from_api("/market/" + symbol);
    } catch (...) {
        // 包装异常，保留原始异常
        std::throw_with_nested(
            DataException(std::format("Failed to fetch data for {}", symbol))
        );
    }
}

// 顶层函数
Portfolio update_portfolio(const Portfolio& p) {
    try {
        auto data = get_market_data("AAPL");
        return p.update(data);
    } catch (...) {
        std::throw_with_nested(
            BusinessException("Portfolio update failed")
        );
    }
}
```

Carol还写了一个工具来打印完整的嵌套异常链：

```cpp
// 递归打印嵌套异常
void print_nested_exception(const std::exception& e, int level = 0) {
    std::cerr << std::string(level * 2, ' ') << e.what() << '\n';

    try {
        std::rethrow_if_nested(e);
    } catch (const std::exception& nested) {
        print_nested_exception(nested, level + 1);
    }
}
```

现在的错误输出变成了：

```
BusinessException: Portfolio update failed
  DataException: Failed to fetch data for AAPL
    NetworkException: Network unavailable
```

黑犬看了新的错误报告，满意地点头："这才对嘛！现在我们能清楚地看到错误是怎么一层层传播的。把这个发给数据供应商！下次这种问题不要再报到我这里来了，忙着呢！"

## 🌅Carol的周末反思

周六早上，Carol终于可以睡个懒觉。醒来时已经是中午，她泡了杯咖啡，坐在露台上点了一支烟，在仔细复盘这一周的经历。

手机响了，是黑犬发来的微信消息：

> "Carol，这周辛苦了。你的异常处理系统让SigmaX的稳定性提升了一个量级。董事会今天开会，所有人都对你的工作赞不绝口。下周一我会宣布给整个QD组增发年终特别奖金💰，你拿双份！"

Carol笑了笑，回复："老板，下次再给我留这种烂摊子，奖金得三倍。"

黑犬秒回："😂成交！哪让你是我们公司独一无二的大宝贝呢😘需要什么资源就和我说，我是你最坚定的后盾！"

Carol放下手机，感受到了黑犬的油腻之后瞬间有种想呕吐🤮的感觉。

Carol打开笔记本，开始写本周的技术博客。标题是：

**《从无声崩溃到优雅失败：现代C++异常处理的艺术》**

她知道，作为CTO，这样的战役还会有很多。但每一次都是让SigmaX变得更强的契机，也是让自己技术力更强的机会。

屋里传来轻快的音乐，Carol端着咖啡，嘴角带着微笑。**错误是不可避免的，但处理错误的方式，决定了一个系统的专业程度。**

下周，SigmaX公司迎来神秘新角色🔍。

## 📒补充说明

本周学习的5个核心异常处理技术，是C++工程中的关键实践：

1. **异常层次结构 + std::source_location** - 精确定位错误
2. **Expected<T,E>** - 零开销的函数式错误处理
3. **std::error_code** - 系统级错误的标准机制
4. **RAII + Transaction** - 异常安全与资源管理
5. **exception_ptr + 嵌套异常** - 复杂场景的异常传播

这些模式的共同目标是：**让错误变得可预测、可处理、可追溯**。在生产环境中，"优雅的失败"比"隐秘的成功"更有价值。很多公司面试时异常处理总是一笔带过，但是工作过的同学都知道实际上真正把玩具项目和工业级生产系统区分开的，不是算法和核心业务代码，而是规范的IO和异常处理体系、以及部署和发布的规范化，毕竟这两个技术决定了项目长期维护的难易程度，这也是为什么我决定用两周的时间专门讲这两块的内容的原因。

至此，我们已经完成了C++基础中IO和异常处理的全部核心内容。从文件系统到序列化，从流管理到错误处理，SigmaX的技术栈已经达到了现代C++的行业标准,如果各位考虑构建自己的C++项目时，也请参考SigmaX的做法(不要脸的笑😊)。

下周，我们将从技术的视角中短暂跳出，迎来SigmaX公司的一位神秘新角色并以一种全新的视角学习计算机科学中最重要的高等数学之一 -- **线性代数**。

本周代码已经上传到Github仓库🔗：[https://github.com/shuheng-mo/qd-study-plan-104wk.git](https://github.com/shuheng-mo/qd-study-plan-104wk.git)，欢迎Star⭐、贡献代码或issue。

**下周预告：W09 - 量化必备的线性代数知识（上）**

👋各位下周五见，SigmaX的故事还远未结束，量化需要的知识也不仅仅局限于编程技术，敬请期待下！
