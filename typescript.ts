/*
########################
### TypeScript language compiled to JavaScript
### First version - 2012, version 0.8


#########################
### TypeScript is superset of JavaScript - introduce new syntax invalid from JS perspective
### TypeScript comes with compiler (tsc) written in TypeScript
### TypeScripts claims that there is no runtime overhead
### The single one structure created by compiler in runtime is Enum
*/






// Simple/Atomic types ###
{
    const a: string= "I am str"
    const b: boolean = true
    const c: number = 12
    const d: number = 1.2

    const strs: string[] = ['a','b']
    const nums: number[] = [1,2,3]
}







// Dictionaries/Map/Tuples
{
    const dic_nums: Map<number, number> = new Map()
    dic_nums.set(1, 2).set(2, 1.2)

    const dic_strs: Map<string, string> = new Map()
    dic_strs.set('a','a').set('b','b')

    type User = {}
    const user_orders: Map<User, number[]> = new Map()
    user_orders.set({}, [1,2,3]).set({}, [2,3,4])

    const dic_strs_obj: Record<string, string> = {'a':'a','b':'b'}
    dic_strs_obj['c'] = 'c'

    // Set
    const set_nums: Set<string> = new Set(['DRY', 'DRY'])

}








// Tuples/Records/Structs/NamedTuple
{  

    // Tuple
    const point: [number, number] = [1,2]

    // Records/Structs/NamedTuple
    type User = {
        name: string
        last_name: string
    }
    const anders: User = {name: 'Anders', last_name: 'TypeScript'}

    // we can use class approach
    class UserClass {
        name: string
        last_name: string
        constructor(name: string, last_name: string) {
            this.name = name;
            this.last_name = last_name
        }
    }
    const anders_by_class = new UserClass('Anders', 'TypeScript')

}










// #### Union (OR)
{
    let union: string | number = 1
    union = 'aa' // ok
    union = 1.2 // ok
    union = true // error

    // compose unions
    const unions: (number | string)[] = [1, 'a', 2, 'b']
    const dict_union: Record<string | number, string> = {
        1: 'a',
        'key': 'b'
    }
    dict_union['key2'] = 'c'
}







// Intersection (AND)
{
    type A = {a: string}
    type B = {b: string}
    type C = A & B
    const c: C = {a: 'a', b: 'b'}
}









// Optional/Nullable
{
    let x: number | null = 1
    x = null

    type Nullable<X> = X | null
    
    let y: Nullable<number> = 1
    y = null
}










// Any and Gradual types
{
    let x: any = 'a'
    x = 'b'
    x = 1
}








// Type aliases
{
type Grade = number
type Name = string
type DateBirth = Date

type Student = {
    name: Name
    last_name: Name
    birth: DateBirth
}

type School = Map<Student, Grade[]>

const batman: Student = {name:'Bruce', last_name:'Wayne', birth: new Date(2000,10,10)}
const joker: Student = {name:"Jack", last_name:"Napier", birth: new Date(2000,10,10)}
const school: School = new Map()
school.set(batman,[1,3,5])
school.set(joker, [5,5,5])

}










// ### Function types annotations
{   
    type Comparator = (x: number, y: number) => boolean
    function compare(comparator: Comparator){
        return (x: number, y: number) => comparator(x,y)
    }

    const is_bigger = compare((x,y) => x > y)
    is_bigger(1,2) // False
    is_bigger(4,3) // True
}









// type inference
{
    function who_am_i(x: string) {
        return x
    }

    function who_am_i_second(x: string, y: number) {
        return x + y
    }

    function who_am_i_third(x: Map<string, string>, prefix: string) {
        const new_map = new Map<string, string>();
        for (const [key, value] of x) {
            new_map.set(key, `${prefix}${value}`)
        }
        return new_map;
    }

    function who_am_i_fourth(x: Record<string, number>, key: string){
        return x[key]
    }

    function who_am_i_fifth(){
        return {
            'a': 1,
            'b': true
        } as const
    }

    function who_am_i_sixth(x: string | string[]){
        if (Array.isArray(x)){
            return ''.concat(...x)
        } else {
            return x
        }
    }
}










// ### Literal types
{
    type TeamMember = 'Batman' | 'Robin'
    let batman: 'Batman' = 'Batman'
    batman = 'Joker' 

    let bat_team_member: TeamMember = 'Robin'
    bat_team_member = 'Joker'

    function want_literal(x: TeamMember){
        switch (x) {
            case 'Batman':
                return 'This city needs me'
            case 'Robin':
                return 'Holy...'
            default:
                return 'Runtime allows the Joker'
        
        }
    }
    want_literal('Joker')
}








// ### Generics
{

    function append<T extends number | string>(x: T, y: T): T {
        return x as any + y
    }
    const x: string = append('a', 'a')
    const y: number = append(1, 2)
    append(1, 'a') // error

    function val<Key extends PropertyKey, Value>(dict: Record<Key, Value>, key: Key){
        return dict[key]
    }
    const val1 = val({'a': 1}, 'a') // number
    const val2 = val({'a':'b'}, 'a') // string
    const val3 = val({'a':'b'}, 'c') // string

}












// ### User-defined generic
{
    type Mappable<IN> = {
        map: (f: (x: IN) => any) => Mappable<any>
    }

    class Arr<IN> implements Mappable<IN> {
        list: IN[]
        constructor(list: IN[]){
            this.list = list
        }
        map<OUT>(f: (x: IN) => OUT) {
            return new Arr(this.list.map(f))
        }
    }
    const x = new Arr([1,2,3,4]) //?
    const y = x.map(n => n+1) //?
    const z = y.map(String) //?
}












// ### Type Guards
{
    function is_str_list(val: unknown[]): val is string[]{
        for (const el of val) {
            if (typeof el !== 'string') {
                return false
            }
        }
        return true
    }
  

    function get_list_from_third_party(list: unknown[]){
        if (is_str_list(list)){
            return list
        }
        throw Error('Not a str list')
    }
    let xs: unknown[] = ['a','b'];
    const xss = get_list_from_third_party(xs)

    type Power = {
        name: string
        level: number
    }
    type SuperHero = {
        name: string
        powers: Power[]
    }
    
    type Villain = {
        name: string
        powers: Power[]
    }

    function is_superhero(x: object): x is SuperHero {
        return 'name' in x && 'powers' in x
    }

    const superman: SuperHero = {
        name:"Superman",
        powers:[{name:'flying', level: 10}]
    }
    const lex: Villain = {
        name:"Lex Luthor",
        powers: [{name:'brain', level: 10}]
    }

    if (is_superhero(lex)) {
        lex //?
    }
}









// ### Structural/Nominal types
{
    // nominal?
    class SuperHero {
        name: string
    }
    class Villain {
        name: string
    }
    const superman = new SuperHero()
    superman.name = 'Clark kent'

    const villain: Villain = superman; // works as structural 🦆

}












// ### Type transformations

// conditional and index types

type UnWrap<T> = T extends Promise<infer X> ? X : T
type Inside = UnWrap<Promise<string>>

// mapped types
type RemoveField<T, FieldTypeToRemove> = Pick<T, {
    [K in keyof T]: T[K] extends FieldTypeToRemove ? never : K
}[keyof T]>
type A = {a: 1, b: 2}
type AA = RemoveField<A, 2>

// and more crazy staff












/// ### Comparison
/**
 * 
 * """
👉 Gradual typing
👉 Is superset and has syntax above base language (JS)
👉 Needs compilation (but there is a plan to ship annotations to JS)
👉 Nominal types support - limited
👉 Structural types support as default 🦆
👉 No need to use class syntax, in most there are better ways
👉 Allows for heavy type transformations
👉 Type syntax similar to C# 

There is ECMAScript proposal for introduction type annotations into JS
If this will be accepted JS will be transformed into TypeScript
TypeScript most probably will convert into type checker like MyPy did
But if part of the syntax will be not expressed in JS it will remain as its superset but with less overhead

 */


